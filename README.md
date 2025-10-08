# Quiz App

A simple and interactive multiple-choice quiz application built with Flask. Users can take quizzes, get immediate feedback on their performance, and add new questions to the database.

## Features

- Take multiple-choice quizzes
- Get immediate feedback and scores
- Add new questions through a user-friendly interface
- Modern and responsive UI
- Score tracking and performance feedback
- Easy to extend with new features

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the files
2. Navigate to the project directory
3. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you're in the project directory and your virtual environment is activated
2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. **Taking a Quiz**:
   - Click on "Take Quiz" from the navigation menu
   - Answer all questions by selecting one option for each
   - Submit your answers to see your score

2. **Adding Questions**:
   - Click on "Add Question" from the navigation menu
   - Fill in the question text, four options, and select the correct answer
   - Submit the form to add the question to the database

## Project Structure

```
quiz_app/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── static/
│   └── style.css      # Custom CSS styles
└── templates/
    ├── base.html      # Base template
    ├── index.html     # Home page
    ├── quiz.html      # Quiz page
    ├── add_question.html  # Add question page
    └── result.html    # Quiz results page
```

## Extending the Project

You can extend this project by:
- Adding user authentication
- Creating different categories of questions
- Implementing a timer feature
- Adding a leaderboard
- Creating different difficulty levels
- Adding question randomization

## License

This project is open source and available under the MIT License. 