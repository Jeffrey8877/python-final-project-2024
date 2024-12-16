// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Timer functionality
    setupTimer();

    // Form validation
    setupFormValidation();

    // Quiz interaction
    setupQuizInteraction();
});

function setupTimer() {
    const timerElement = document.getElementById('quiz-timer');
    if (!timerElement) return;  // No timer needed for this page

    const timeLimit = parseInt(timerElement.dataset.timeLimit);
    if (!timeLimit) return;

    let timeLeft = timeLimit * 60;  // Convert to seconds
    const timerDisplay = document.getElementById('time-display');

    const timer = setInterval(() => {
        timeLeft--;

        // Format time as MM:SS
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent =
            `${minutes}:${seconds.toString().padStart(2, '0')}`;

        // Warning when 1 minute remaining
        if (timeLeft === 60) {
            timerDisplay.style.color = 'red';
            showWarning('1 minute remaining!');
        }

        // Auto-submit when time's up
        if (timeLeft <= 0) {
            clearInterval(timer);
            const form = document.getElementById('quiz-form');
            if (form) form.submit();
        }
    }, 1000);
}

function setupFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    showError(field, 'This field is required');
                } else {
                    clearError(field);
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

function setupQuizInteraction() {
    const quizForm = document.getElementById('quiz-form');
    if (!quizForm) return;  // Not on a quiz page

    // Highlight selected options
    const options = document.querySelectorAll('.option');
    options.forEach(option => {
        option.addEventListener('click', function() {
            // Find the radio input within this option
            const radio = this.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;

            // Remove highlight from other options in this question
            const questionContainer = this.closest('.question-container');
            questionContainer.querySelectorAll('.option').forEach(opt => {
                opt.classList.remove('selected');
            });

            // Add highlight to selected option
            this.classList.add('selected');
        });
    });
}

function showWarning(message) {
    const warning = document.createElement('div');
    warning.className = 'alert alert-warning';
    warning.textContent = message;

    const container = document.querySelector('.container');
    container.insertBefore(warning, container.firstChild);

    // Remove warning after 5 seconds
    setTimeout(() => warning.remove(), 5000);
}

function showError(field, message) {
    // Clear any existing error
    clearError(field);

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
    field.classList.add('error');
}

function clearError(field) {
    const parent = field.parentNode;
    const errorDiv = parent.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
        field.classList.remove('error');
    }
}