import { GoogleAuthProvider, getAuth, signInWithPopup } from "firebase/auth";
import app from "./firebase";
import request_caller from "../api/request.handler";
import store from "../store/store";
import { setUser } from "../store/auth/authSlice";

const googleProvider = new GoogleAuthProvider();
const auth = getAuth(app);
export const signInWithGoogle = () => signInWithPopup(auth, googleProvider);

function oauth_request(oauth_res, isStaff) {
  const body = {
    obj_data: oauth_res,
  };

  const auth_urls = isStaff ? "/support_login" : "/login";

  request_caller({
    endpoint: auth_urls,
    data: body,
    successToast: true,
    isAuthenticated: false,
  })
    .then((response) => {
      if (response.success) {
        store.dispatch(setUser(response.data.user));
        localStorage.setItem("token", response.data.token);
        localStorage.setItem("key", response.data.key);
        window.location.href = "/";
      }
    })
    .catch((_) => {});
}

const pop_up_error_codes = [
  "auth/cancelled-popup-request",
  "auth/popup-closed-by-user",
];

//============== Google OAuth ==============//
export const googleAuthHandler = async (isStaff) => {
  try {
    const googleRes = await signInWithGoogle();
    oauth_request(googleRes, isStaff);
  } catch (error) {
    if (pop_up_error_codes.includes(error.code)) {
      alert("Google pop up window closed by you");
    }
    console.log(error, error.code);
  }
};
