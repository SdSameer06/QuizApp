from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from quiz_db import db, User, Question, init_db, add_question, get_questions_by_difficulty
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize database
db = SQLAlchemy(app)

# Database Models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    wrong_answers = db.Column(db.String(600), nullable=False)  # Stored as comma-separated values
    difficulty = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        wrong_answers_list = self.wrong_answers.split(',')
        options = wrong_answers_list + [self.correct_answer]
        return {
            'id': self.id,
            'question': self.question,
            'options': options,
            'correct_answer': self.correct_answer
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()

# Create results directory if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Registration successful!'})

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})

    return render_template('login.html')

@app.route('/check_auth')
def check_auth():
    # For demonstration, always return not authenticated
    return jsonify({
        'authenticated': False
    })

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@app.route('/get_questions')
def get_questions():
    difficulty = request.args.get('difficulty')
    if not difficulty:
        return jsonify({
            'success': False,
            'message': 'Difficulty not specified'
        })
    
    questions = Question.query.filter_by(difficulty=difficulty).all()
    if questions:
        return jsonify({
            'success': True,
            'questions': [q.to_dict() for q in questions]
        })
    
    return jsonify({
        'success': False,
        'message': f'No questions available for {difficulty} difficulty'
    })

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        if request.is_json:
            difficulty = request.json.get('difficulty')
        else:
            difficulty = request.form.get('difficulty')
            
        if difficulty:
            questions = Question.query.filter_by(difficulty=difficulty).all()
            if questions:
                return jsonify({
                    'success': True,
                    'message': 'Questions loaded successfully'
                })
            return jsonify({
                'success': False,
                'message': f'No questions available for {difficulty} difficulty'
            })
    
    return render_template('quiz.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get form data
        answers = {}
        difficulty = request.form.get('difficulty')
        
        # Collect answers
        for key, value in request.form.items():
            if key.startswith('answer_'):
                question_index = int(key.split('_')[1])
                answers[question_index] = value

        # Calculate score (simplified version)
        score = len(answers)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_file = f'quiz_result_{timestamp}.txt'
        
        # Save results
        with open(os.path.join('results', result_file), 'w') as f:
            f.write(f'Quiz Results\n')
            f.write(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'Difficulty: {difficulty}\n')
            f.write(f'Score: {score}\n\n')
            
            for index, answer in answers.items():
                f.write(f'Question {index + 1}: Your answer: {answer}\n')

        return jsonify({
            'success': True,
            'message': f'Quiz completed! Score: {score}',
            'score': score,
            'total': len(answers)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error submitting quiz: {str(e)}'
        })

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            question_text = request.form.get('question')
            difficulty = request.form.get('difficulty')
            correct_answer = request.form.get('correct_answer')
            wrong_answers = [
                request.form.get('wrong_answer1'),
                request.form.get('wrong_answer2'),
                request.form.get('wrong_answer3')
            ]
            
            # Create new question
            new_question = Question(
                question=question_text,
                correct_answer=correct_answer,
                wrong_answers=','.join(wrong_answers),
                difficulty=difficulty
            )
            
            db.session.add(new_question)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Question added successfully!'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error adding question: {str(e)}'
            })
            
    return render_template('add.html')

@app.route('/view_results')
def view_results():
    results = []
    if os.path.exists('results'):
        for filename in os.listdir('results'):
            if filename.startswith('quiz_result_'):
                try:
                    with open(os.path.join('results', filename), 'r') as f:
                        content = f.read()
                        results.append({
                            'filename': filename,
                            'content': content
                        })
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                    continue
    
    return render_template('view_results.html', results=results)

@app.route('/list_questions')
@login_required
def list_questions():
    questions = Question.query.all()
    return render_template('list_questions.html', questions=questions)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True) 