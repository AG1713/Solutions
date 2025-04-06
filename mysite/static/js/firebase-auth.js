// Import the functions you need from the SDKs you need
// import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCw6JFre8IzjlcLfTWPHZaXMlHkG6FipG0",
  authDomain: "xenova-ea917.firebaseapp.com",
  projectId: "xenova-ea917",
  storageBucket: "xenova-ea917.firebasestorage.app",
  messagingSenderId: "1022603031826",
  appId: "1:1022603031826:web:1bc079bf02a826d384efcb",
  measurementId: "G-7SRT77X37X"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Google Sign-In Function
function googleLogin() {
  signInWithPopup(auth, provider)
    .then((result) => {
      console.log("User Signed In:", result.user);
      window.location.href = "/home"; // Redirect to home after login
    })
    .catch((error) => {
      console.error("Sign-in error:", error);
    });
}

// Logout Function
function logout() {
  signOut(auth)
    .then(() => {
      console.log("User Signed Out");
      window.location.href = "/login"; // Redirect to login after logout
    })
    .catch((error) => {
      console.error("Sign-out error:", error);
    });
}

// Attach functions to buttons
document.getElementById("google-login-btn").addEventListener("click", googleLogin);
document.getElementById("logout-btn").addEventListener("click", logout);