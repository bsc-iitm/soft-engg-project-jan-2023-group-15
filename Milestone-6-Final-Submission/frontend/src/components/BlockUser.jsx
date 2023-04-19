import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { setStaffList } from "../store/auth/authSlice";
import request_caller from "../api/request.handler";

function BlockUser({ user }) {
  const staffList = useSelector((state) => state.auth.staffList);
  const current_user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();
  const blockUser = () => {
    request_caller({
      method: "post",
      endpoint: "/user/block",
      data: { user_id: user.id },
      successToast: true,
    }).then((res) => {
      if (res.success) {
        if (user.role == "SUPPORT_STAFF" && staffList) {
          const lc_staff = [...staffList];
          const updated = lc_staff.filter((lc) => lc.id !== user.id);
          dispatch(setStaffList(updated));
        }
      }
    });
  };

  return (
    (current_user.role === "SUPPORT_STAFF" || current_user.role == "ADMIN") && (
      <>
        <button
          className="btn btn-outline-secondary mx-2"
          onClick={() => blockUser()}
        >
          Block {user?.username ?? "User"}
        </button>
      </>
    )
  );
}

export default BlockUser;
