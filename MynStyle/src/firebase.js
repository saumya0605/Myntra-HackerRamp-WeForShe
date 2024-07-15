// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

//database adding
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
//add firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBng8b1kuBoFU7bPiRjoQa6cRs39oTgEco",
  authDomain: "mynstyle-b3b59.firebaseapp.com",
  projectId: "mynstyle-b3b59",
  storageBucket: "mynstyle-b3b59.appspot.com",
  messagingSenderId: "327607950460",
  appId: "1:327607950460:web:fa22a8b0005eaf7294bdf9",
  measurementId: "G-PLTGBTXFJ8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const database = getDatabase(app);

export { auth, db, database };
