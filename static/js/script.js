// Toast notification handling
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toastContainer.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s forwards';
        setTimeout(() => {
            toast.remove();
            if (toastContainer.children.length === 0) {
                toastContainer.remove();
            }
        }, 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// Form submission handling
document.addEventListener('DOMContentLoaded', function() {
    // Login form handling
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(loginForm);
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Login successful!', 'success');
                    window.location.href = '/';
                } else {
                    showToast(data.message || 'Login failed', 'error');
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    }

    // Registration form handling
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(registerForm);
            if (formData.get('password') !== formData.get('confirm_password')) {
                showToast('Passwords do not match', 'error');
                return;
            }
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Registration successful!', 'success');
                    window.location.href = '/login';
                } else {
                    showToast(data.message || 'Registration failed', 'error');
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    }

    // Quiz form handling
    const quizForm = document.getElementById('quizForm');
    if (quizForm) {
        quizForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(quizForm);
            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    showToast(`Quiz completed! Score: ${data.score}/${data.total}`, 'success');
                    window.location.href = '/view_results';
                } else {
                    showToast(data.message || 'Failed to submit quiz', 'error');
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    }

    // Add question form handling
    const addQuestionForm = document.getElementById('addQuestionForm');
    if (addQuestionForm) {
        addQuestionForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(addQuestionForm);
            try {
                const response = await fetch('/add', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.success) {
                    showToast('Question added successfully!', 'success');
                    addQuestionForm.reset();
                } else {
                    showToast(data.message || 'Failed to add question', 'error');
                }
            } catch (error) {
                showToast('An error occurred', 'error');
            }
        });
    }
}); 