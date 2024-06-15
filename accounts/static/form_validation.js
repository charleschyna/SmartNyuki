
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('signupForm');

    if (form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault();
            } else {
                var submitButton = event.target.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.textContent = 'Signing up...';
            }
        });
    }

    var googleButton = document.querySelector('.social-btn.google');
    if (googleButton) {
        googleButton.addEventListener('click', function() {
            alert('Redirecting to Google signup...');
        });
    }
});

function validateForm() {
    var username = document.getElementById('username').value.trim();
    var email = document.getElementById('email').value.trim();
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var errorMessages = [];

    if (username === '') {
        errorMessages.push('Username is required.');
    }

    if (email === '') {
        errorMessages.push('Email is required.');
    }

    if (password1 === '') {
        errorMessages.push('Password is required.');
    }

    if (password1 !== password2) {
        errorMessages.push('Passwords do not match.');
    }

    
    displayErrorMessages(errorMessages);

    return errorMessages.length === 0;
}

function displayErrorMessages(messages) {
    var errorContainer = document.getElementById('error-messages');

    errorContainer.innerHTML = '';

    if (messages.length > 0) {
        messages.forEach(function(message) {
            var errorMessage = document.createElement('div');
            errorMessage.textContent = message;
            errorContainer.appendChild(errorMessage);
        });
    }
}
