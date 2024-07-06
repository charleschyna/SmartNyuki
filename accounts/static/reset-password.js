// Import the required Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, sendPasswordResetEmail } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

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

// Function to handle password reset
const handlePasswordReset = async (email) => {
    const messageDiv = document.getElementById('message');
    try {
        await sendPasswordResetEmail(auth, email);
        messageDiv.textContent = 'Password reset email sent!';
        messageDiv.style.color = 'green';
    } catch (error) {
        console.error('Error sending password reset email:', error);
        messageDiv.textContent = 'Failed to send password reset email: ' + error.message;
        messageDiv.style.color = 'red';
    }
};

// Add a listener for the submit event on the form
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const resetEmail = document.getElementById('reset-email').value;
        handlePasswordReset(resetEmail);
    });
});
