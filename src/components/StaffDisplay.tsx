import React from 'react';
import '../styles/StaffDisplay.css';

export interface StaffProps {
    name: string;
    position: string;
    photo: string;
    email: string;
    phone: string;
}

interface staff {
  staffList : StaffProps[];
}

const StaffDisplay: React.FC<staff> = ({ staffList }) => {

  return (
    <div className="staff-container">
      {staffList.map((staff, index) => (
        <div className="staff-box" key={index}>
          <img src={staff.photo} alt={staff.name} className="staff-photo"/>
          <div className="staff-details">
            <div className="staff-name">{staff.name}</div>
            <div className="staff-position">{staff.position}</div>
            <div className="staff-contact">
              <div className="staff-email">{staff.email}</div>
              <div className="staff-phone">{staff.phone}</div>
            </div>
            <button className="staff-edit-button">Edit</button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StaffDisplay;
