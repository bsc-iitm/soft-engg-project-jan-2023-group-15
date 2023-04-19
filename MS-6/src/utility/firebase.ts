// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAdDP_861W8ziyi1JABEsIV79Haf2HwvDo",
  authDomain: "se-project-383806.firebaseapp.com",
  projectId: "se-project-383806",
  storageBucket: "se-project-383806.appspot.com",
  messagingSenderId: "986425424217",
  appId: "1:986425424217:web:c753ac24ad19a784c83448",
  measurementId: "G-ZFPGX5DN69"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export default app;