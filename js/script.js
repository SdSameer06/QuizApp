// DOM Elements
const sections = document.querySelectorAll('.section');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const quizSection = document.getElementById('quizSection');
const addQuestionForm = document.getElementById('addQuestionForm');
const resultsSection = document.getElementById('resultsSection');
const userGreeting = document.getElementById('userGreeting');
const logoutButton = document.getElementById('logoutButton');

// Show specific section and hide others
function showSection(sectionId) {
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

// Toast notification
function showToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = `toast ${isError ? 'error' : 'success'}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// User Authentication
function register(event) {
    event.preventDefault();
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    if (users.some(user => user.username === username)) {
        showToast('Username already exists', true);
        return;
    }
    
    users.push({ username, password });
    localStorage.setItem('users', JSON.stringify(users));
    showToast('Registration successful!');
    showSection('loginSection');
}

function login(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find(u => u.username === username && u.password === password);
    
    if (user) {
        localStorage.setItem('currentUser', username);
        userGreeting.textContent = `Welcome, ${username}!`;
        showToast('Login successful!');
        showSection('homeSection');
    } else {
        showToast('Invalid credentials', true);
    }
}

function logout() {
    localStorage.removeItem('currentUser');
    showToast('Logged out successfully');
    showSection('loginSection');
}

// Quiz Functions
function loadQuiz(difficulty) {
    const questions = quizQuestions[difficulty];
    let currentQuestionIndex = 0;
    let score = 0;
    
    function displayQuestion() {
        const question = questions[currentQuestionIndex];
        const quizContent = document.getElementById('quizContent');
        
        quizContent.innerHTML = `
            <h3>Question ${currentQuestionIndex + 1}/${questions.length}</h3>
            <p>${question.question}</p>
            <div class="options">
                ${question.options.map((option, index) => `
                    <button onclick="selectAnswer(${index})">${option}</button>
                `).join('')}
            </div>
        `;
    }
    
    window.selectAnswer = function(selectedIndex) {
        const question = questions[currentQuestionIndex];
        if (selectedIndex === question.correct) {
            score++;
            showToast('Correct answer!');
        } else {
            showToast('Wrong answer', true);
        }
        
        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            displayQuestion();
        } else {
            finishQuiz(score, questions.length, difficulty);
        }
    };
    
    displayQuestion();
}

function finishQuiz(score, total, difficulty) {
    const percentage = (score / total) * 100;
    const result = {
        date: new Date().toISOString(),
        score,
        total,
        percentage,
        difficulty
    };
    
    const results = JSON.parse(localStorage.getItem('quizResults') || '[]');
    results.push(result);
    localStorage.setItem('quizResults', JSON.stringify(results));
    
    showSection('resultsSection');
    displayResults();
}

function displayResults() {
    const results = JSON.parse(localStorage.getItem('quizResults') || '[]');
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p>No quiz results yet.</p>';
        return;
    }
    
    resultsContainer.innerHTML = results.map(result => `
        <div class="result-card">
            <h4>Quiz Result</h4>
            <p>Date: ${new Date(result.date).toLocaleDateString()}</p>
            <p>Difficulty: ${result.difficulty}</p>
            <p>Score: ${result.score}/${result.total}</p>
            <p>Percentage: ${result.percentage.toFixed(2)}%</p>
            <span class="badge ${result.percentage >= 70 ? 'pass' : 'fail'}">
                ${result.percentage >= 70 ? 'PASS' : 'FAIL'}
            </span>
        </div>
    `).join('');
}

// Add Question
function addQuestion(event) {
    event.preventDefault();
    const question = document.getElementById('questionText').value;
    const difficulty = document.getElementById('questionDifficulty').value;
    const options = [
        document.getElementById('option1').value,
        document.getElementById('option2').value,
        document.getElementById('option3').value,
        document.getElementById('option4').value
    ];
    const correct = parseInt(document.getElementById('correctAnswer').value) - 1;
    
    const newQuestion = {
        id: Date.now(),
        question,
        options,
        correct
    };
    
    const customQuestions = JSON.parse(localStorage.getItem('customQuestions') || '{}');
    if (!customQuestions[difficulty]) {
        customQuestions[difficulty] = [];
    }
    customQuestions[difficulty].push(newQuestion);
    localStorage.setItem('customQuestions', JSON.stringify(customQuestions));
    
    showToast('Question added successfully!');
    event.target.reset();
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    registerForm.addEventListener('submit', register);
    loginForm.addEventListener('submit', login);
    logoutButton.addEventListener('click', logout);
    addQuestionForm.addEventListener('submit', addQuestion);
    
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        userGreeting.textContent = `Welcome, ${currentUser}!`;
        showSection('homeSection');
    } else {
        showSection('loginSection');
    }
}); 