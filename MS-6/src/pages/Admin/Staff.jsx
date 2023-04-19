import React, {useEffect} from "react";
import NavBar from "../../components/NavBar";
import "../../styles/Profile.css";
import StaffDisplay from "../../components/StaffDisplay";
import { useSelector, useDispatch } from "react-redux";
import { setStaffList } from "../../store/auth/authSlice";
import request_caller from "../../api/request.handler";
import AddStaff from "../../components/AddStaff";

const Staff = () => {
  const staffList = useSelector((state) => state.auth.staffList);
  const didOnce = React.useRef(false);
  const dispatch = useDispatch();
  useEffect(() => {
    if (!staffList && !didOnce.current) {
      didOnce.current = true;
      request_caller({
        method: "get",
        endpoint: "/staff",
        data: {},
        successToast: false,
      })
        .then((res) => {
          dispatch(setStaffList(res.data));
        })
        .catch((_err) => {
          dispatch(setStaffList([]));
        });
    }
  }, [staffList]);

  return (
    <div className="">
      <NavBar />
      <div className="pt-4">
        {staffList && staffList.length === 0 && (
          <div className="text-center">No Staffs found</div>
        )}
        {staffList && staffList.length !== 0 && (
          <div className="container">
            <div className="flex-row justify-content-between">
              <h2>Your Force</h2>
              <AddStaff />
            </div>
            <StaffDisplay />
          </div>
        )}
      </div>
    </div>
  );
};

export default Staff;
