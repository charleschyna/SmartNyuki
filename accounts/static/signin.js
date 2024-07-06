// Import the required Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, sendPasswordResetEmail } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCiraum9gVPXkgP3KgEXk3WMhEb64XZjZE",
    authDomain: "project-login2-6c049.firebaseapp.com",
    projectId: "project-login2-6c049",
    storageBucket: "project-login2-6c049.appspot.com",
    messagingSenderId: "865918979599",
    appId: "1:865918979599:web:b0cb8e55945a81921d9d7a"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Function to handle sign-in
const handleSignIn = async (email, password) => {
    const messageDiv = document.getElementById('message');
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        console.log('Signed in:', userCredential.user);

        // Display success message
        messageDiv.textContent = 'User signed in successfully!';
        messageDiv.style.color = 'green';

        // Redirect to dashboard (change to your desired path)
        window.location.href = 'dashboard';  // Replace '/dashboard/' with your actual Django dashboard URL
    } catch (error) {
        console.error('Error signing in:', error);
        messageDiv.textContent = 'Failed to sign in: ' + error.message;
        messageDiv.style.color = 'red';
    }
};



// Add a listener for the submit event on the sign-in form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.form');
    // Adjust the form submit handler to handle AJAX response
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const emailInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
    
        if (emailInput && passwordInput) {
            const email = emailInput.value;
            const password = passwordInput.value;
            try {
                const response = await fetch('/accounts/signin/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest', // Add this header to indicate an AJAX request
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ username: email, password }),
                });
                const data = await response.json();
                if (response.ok) {
                    // Redirect to the URL returned from Django
                    window.location.href = data.redirect_url;
                } else {
                    console.error('Failed to sign in:', data.error);
                    messageDiv.textContent = 'Failed to sign in: ' + data.error;
                    messageDiv.style.color = 'red';
                }
            } catch (error) {
                console.error('Error signing in:', error);
                messageDiv.textContent = 'Failed to sign in: ' + error.message;
                messageDiv.style.color = 'red';
            }
        } else {
            console.error('Form elements not found.');
        }
    });
});
