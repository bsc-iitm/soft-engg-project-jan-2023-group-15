import React from "react";
import "../styles/StaffDisplay.css";
import { useSelector, useDispatch } from "react-redux";
import request_caller from "../api/request.handler";
import { setStaffList } from "../store/auth/authSlice";
import BlockUser from "./BlockUser";

const StaffDisplay = () => {
  const staffList = useSelector((state) => state.auth.staffList);
  const dispatch = useDispatch();

  const removeAsStaff = (staff) => {
    request_caller({
      method: "delete",
      endpoint: "/staff",
      data: { staff_id: staff.id },
      successToast: true,
    }).then((res) => {
      if (res.success) {
        const lc_staff = [...staffList];
        const updated = lc_staff.filter((lc) => lc.id !== staff.id);
        dispatch(setStaffList(updated));
      }
    });
  };

  return (
    <div className="staff-container">
      {staffList?.map((staff, index) => (
        <div className="staff-box" key={index}>
          {staff.profile_picture ? (
            <img
              src={staff.profile_picture}
              alt={staff.full_name}
              className="staff-photo"
            />
          ) : (
            <div
              className="rounded-circle border staff-photo flex-row align-center justify-content-center text-capitalize"
              style={{ fontSize: "60px" }}
            >
              {staff.username?.slice(0, 1)}
            </div>
          )}
          <div className="staff-details">
            <div className="staff-name">{staff.full_name}</div>
            <div className="staff-name">{staff.username}</div>
            <div className="staff-position">{staff.role}</div>
            <div className="staff-contact">
              <div className="staff-email">{staff.email}</div>
            </div>
            <button className="btn btn-outline-secondary mx-2 mb-2" onClick={()=>removeAsStaff(staff)}>
              Remove as staff
            </button>
            <BlockUser user={staff} />
          </div>
        </div>
      ))}
    </div>
  );
};

export default StaffDisplay;
