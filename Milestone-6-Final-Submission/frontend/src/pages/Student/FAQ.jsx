import React, { useEffect } from "react";
import "../../styles/Contents.css";
import Q_A from "../../components/Q_A";
import NavBar from "../../components/NavBar";
import { useSelector, useDispatch } from "react-redux";
import { setFAQs } from "../../store/auth/authSlice";
import request_caller from "../../api/request.handler";
import AddFAQ from "../../components/AddFAQ";
import { Link } from "react-router-dom";

const FAQ = () => {
  const faqs = useSelector((state) => state.auth.faqs);
  const user = useSelector((state) => state.auth.user);
  const didOnce = React.useRef(false);
  const dispatch = useDispatch();
  useEffect(() => {
    if (!faqs && !didOnce.current) {
      didOnce.current = true;
      request_caller({
        method: "get",
        endpoint: "/faq",
        data: {},
        successToast: false,
      })
        .then((res) => {
          dispatch(setFAQs(res.data));
        })
        .catch((_err) => {
          dispatch(setFAQs([]));
        });
    }
  }, [faqs]);

  return (
    <div className="FAQ">
      <NavBar home={"/"} faq={"/FAQ"} profile={"/profile"} staff={""} />
      <div className="pt-4">
        {" "}
        {faqs && faqs.length === 0 && (
          <div className="text-center">No FAQs found</div>
        )}
        {faqs && faqs.length !== 0 && (
          <div className="container">
            <div className="flex-row justify-content-between">
              <h2>Frequently Asked Questions</h2>
              <div className="flex-row align-center">
                {user.role === "ADMIN" && (
                  <Link to="/FAQ/requests" className="btn btn-outline-primary">
                    View Requests
                  </Link>
                )}
                <AddFAQ />
              </div>
            </div>
            <Q_A />
          </div>
        )}
      </div>
    </div>
  );
};

export default FAQ;
