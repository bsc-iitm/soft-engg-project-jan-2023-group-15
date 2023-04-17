import React from "react";
import "../styles/UserDetails.css";

interface UserDetailsProps {
  avatar: string;
  name: string;
  email: string;
  type: string;
  joiningDate: string;
}

const UserDetails: React.FC<UserDetailsProps> = ({
  avatar,
  name,
  email,
  type,
  joiningDate,
}) => {
  return (
    <div className="user-details-container">
      <div className="user-avatar">
        <img src={avatar} alt="User Avatar" />
      </div>
      <div className="user-info">
        <div className="user-name">{name}</div>
        <div className="user-email">{email}</div>
        <div className="user-type">{type}</div>
        <div className="user-joining-date">{joiningDate}</div>
        {/* Add more details here */}
      </div>
    </div>
  );
};

export default UserDetails;
