from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    wrong_answers = db.Column(db.String(600), nullable=False)  # Stored as comma-separated values
    difficulty = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        wrong_answers_list = self.wrong_answers.split(',')
        options = wrong_answers_list + [self.correct_answer]
        random.shuffle(options)
        return {
            'id': self.id,
            'question': self.question,
            'options': options,
            'correct_answer': self.correct_answer,
            'difficulty': self.difficulty
        }

def init_db():
    # Create some sample questions if none exist
    if not Question.query.first():
        sample_questions = [
            {
                'question': 'What is the capital of France?',
                'correct_answer': 'Paris',
                'wrong_answers': ['London,Berlin,Madrid'],
                'difficulty': 'easy'
            },
            {
                'question': 'What is 2 + 2?',
                'correct_answer': '4',
                'wrong_answers': ['3,5,6'],
                'difficulty': 'easy'
            }
        ]
        
        for q in sample_questions:
            question = Question(
                question=q['question'],
                correct_answer=q['correct_answer'],
                wrong_answers=','.join(q['wrong_answers']),
                difficulty=q['difficulty']
            )
            db.session.add(question)
        
        db.session.commit()

def add_question(question_data):
    question = Question(
        question=question_data['question'],
        correct_answer=question_data['correct_answer'],
        wrong_answers=','.join(question_data['wrong_answers']),
        difficulty=question_data['difficulty']
    )
    db.session.add(question)
    db.session.commit()
    return question

def get_questions_by_difficulty(difficulty):
    return Question.query.filter_by(difficulty=difficulty).all()

# Sample questions for testing
sample_questions = [
    {
        'question': 'What is the capital of France?',
        'correct_answer': 'Paris',
        'wrong_answers': ['London', 'Berlin', 'Madrid'],
        'difficulty': 'easy'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'correct_answer': 'Mars',
        'wrong_answers': ['Venus', 'Jupiter', 'Saturn'],
        'difficulty': 'easy'
    },
    {
        'question': 'What is the chemical symbol for gold?',
        'correct_answer': 'Au',
        'wrong_answers': ['Ag', 'Fe', 'Cu'],
        'difficulty': 'medium'
    },
    {
        'question': 'Who painted the Mona Lisa?',
        'correct_answer': 'Leonardo da Vinci',
        'wrong_answers': ['Pablo Picasso', 'Vincent van Gogh', 'Michelangelo'],
        'difficulty': 'medium'
    },
    {
        'question': 'What is the speed of light in meters per second?',
        'correct_answer': '299,792,458',
        'wrong_answers': ['300,000,000', '299,999,999', '299,792,000'],
        'difficulty': 'hard'
    }
]

def add_sample_questions():
    """Add sample questions to the database if it's empty"""
    if Question.query.count() == 0:
        for question_data in sample_questions:
            add_question(question_data) 