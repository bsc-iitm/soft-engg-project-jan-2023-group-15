import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setBlockedUserLists } from "../store/auth/authSlice";
import request_caller from "../api/request.handler";
import "../styles/StaffDisplay.css";

function UnblockUserList() {
  const blocked_user_lists = useSelector(
    (state) => state.auth.blocked_user_lists
  );
  const didOnce = React.useRef(false);
  const dispatch = useDispatch();
  useEffect(() => {
    if (!blocked_user_lists && !didOnce.current) {
      didOnce.current = true;
      request_caller({
        method: "get",
        endpoint: "/user/unblock",
        data: {},
        successToast: false,
      })
        .then((res) => {
          dispatch(setBlockedUserLists(res.data));
        })
        .catch((_err) => {
          dispatch(setBlockedUserLists([]));
        });
    }
  }, [blocked_user_lists]);

  const unblockUser = (staff) => {
    request_caller({
      method: "post",
      endpoint: "/user/unblock",
      data: {
        user_id: staff.id,
      },
      successToast: true,
    }).then((res) => {
      const lc_blocked_user_lists = [...blocked_user_lists];
      const updated = lc_blocked_user_lists.filter((lc) => lc.id !== staff.id);
      dispatch(setBlockedUserLists(updated));
    });
  };

  return (
    <div>
      {blocked_user_lists && blocked_user_lists.length > 0 && (
        <>
          <h5 className="mt-4">Blocked Users</h5>
          <div className="staff-container px-4 py-4">
            {blocked_user_lists?.map((staff, index) => (
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
                  <button
                    className="btn btn-secondary"
                    onClick={(e) => {
                      unblockUser(staff);
                    }}
                  >
                    Unblock {staff.username}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default UnblockUserList;
