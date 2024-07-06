importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

firebase.initializeApp({
  apiKey: "AIzaSyCiraum9gVPXkgP3KgEXk3WMhEb64XZjZE",
  authDomain: "project-login2-6c049.firebaseapp.com",
  projectId: "project-login2-6c049",
  storageBucket: "project-login2-6c049.appspot.com",
  messagingSenderId: "865918979599",
  appId: "1:865918979599:web:b0cb8e55945a81921d9d7a",
});

const messaging = firebase.messaging();

// Optional: Add an event listener to handle background messages
messaging.setBackgroundMessageHandler(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/firebase-logo.png'
  };

  return self.registration.showNotification(notificationTitle,
    notificationOptions);
});
