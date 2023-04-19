import React from "react";
import "../styles/UserDetails.css";
import { useSelector } from "react-redux";
import request_caller from "../api/request.handler";

const UserDetails = () => {
  const user = useSelector((state) => state.auth.user);

  const logoutHandler = (isLogout = true) => {
    request_caller({
      method: "post",
      endpoint: isLogout ? "/logout" : "/user/deactivate",
      data: {},
      successToast: true,
    }).then(() => {
      localStorage.removeItem("token");
      localStorage.removeItem("key");
      window.location.href = "/login";
    });
  };

  return (
    <div className="user-details-container">
      <div className="user-avatar">
        <img src={user?.profile_picture} alt="User Avatar" />
      </div>
      <div className="user-info">
        <div className="user-name">{user?.username}</div>
        <div className="user-name">{user?.full_name}</div>
        <div className="user-email">{user?.email}</div>
        <div className="user-type">{user?.role}</div>
        <div className="user-joining-date">{user?.created_at}</div>
        <div className="p-4">
          <button
            className="btn btn-outline-secondary mx-2"
            onClick={() => logoutHandler(false)}
          >
            Deactivate
          </button>
          <button
            className="btn btn-outline-warning"
            onClick={() => logoutHandler(true)}
          >
            Logout
          </button>
        </div>
        {/* Add more details here */}
      </div>
    </div>
  );
};

export default UserDetails;
