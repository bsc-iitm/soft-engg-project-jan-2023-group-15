import React, { useEffect, useRef, useState } from "react";
import Option1 from "./pages/Student/Student";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import HomePage from "./pages/HomePage";
import FAQ from "./pages/Student/FAQ";
import Profile from "./pages/Student/Profile";
import "./App.css";
import Staff from "./pages/Admin/Staff";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useDispatch, useSelector } from "react-redux";
import { setUser } from "./store/auth/authSlice";
import request_caller from "./api/request.handler";
import Loader from "./components/Loader";
import FAQRequest from "./pages/Admin/FAQRequest";

function ProtectedComponent({ redirect, Component }) {
  return redirect ? <Navigate to="/login" replace /> : Component;
}

function App() {
  const [redirect, setRedirect] = useState(false);
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();
  const didOnce = useRef(false);

  useEffect(() => {
    console.log("====================================");
    console.log(user, didOnce.current);
    console.log("====================================");
    if (!user && !didOnce.current && window.location.pathname !== "/login") {
      didOnce.current = true;
      request_caller({
        method: "get",
        endpoint: "/user",
        successToast: false,
        errorToast: true,
        data: {},
      })
        .then((res) => {
          dispatch(setUser(res.data));
        })
        .catch((_err) => {
          console.log("====================================");
          console.log(_err);
          console.log("====================================");
          dispatch(setUser({}));
          setRedirect(true);
          window.location.href = "/login";
        });
    }
  }, [user, dispatch]);

  return (
    <Router>
      <div className="App">
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
        <Loader />
        <Routes>
          <Route path="/login" element={<HomePage />} />
          {!user && (
            <Route
              path="/"
              element={
                <ProtectedComponent redirect={redirect} Component={<></>} />
              }
            />
          )}
          {user && (
            <>
              <Route
                path="/"
                element={
                  <ProtectedComponent
                    redirect={redirect}
                    Component={<Option1 />}
                  />
                }
              />
              <Route
                path="/FAQ"
                element={
                  <ProtectedComponent redirect={redirect} Component={<FAQ />} />
                }
              />
              <Route
                path="/profile"
                element={
                  <ProtectedComponent
                    redirect={redirect}
                    Component={<Profile />}
                  />
                }
              />
              {/* Admin login */}
              {user.role === "ADMIN" && (
                <>
                  <Route path="/staff" element={<Staff />} />
                  <Route path="/FAQ/requests" element={<FAQRequest />} />
                </>
              )}
            </>
          )}
          <Route path="*" element={<>404 Bro!!!</>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
