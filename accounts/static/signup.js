// Import the required Firebase modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js';
import { getAuth, createUserWithEmailAndPassword, sendEmailVerification } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js';

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

// Function to handle sign-up
const handleSignUp = async (email, password) => {
    const messageDiv = document.getElementById('message');
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        console.log('Signed up:', userCredential.user);

        // Send email verification
        await sendEmailVerification(userCredential.user);

        // Display success message
        messageDiv.textContent = 'User signed up successfully! Please verify your email address.';
        messageDiv.style.color = 'green';
    } catch (error) {
        console.error('Error signing up:', error);
        messageDiv.textContent = 'Failed to sign up: ' + error.message;
        messageDiv.style.color = 'red';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        handleSignUp(email, password);
    });
});

