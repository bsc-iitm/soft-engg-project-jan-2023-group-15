import React, { useEffect } from "react";
import NavBar from "../../components/NavBar";
import "../../styles/Contents.css";
import { useSelector, useDispatch } from "react-redux";
import { setFAQRequests } from "../../store/auth/authSlice";
import request_caller from "../../api/request.handler";
import Q_A_Admin from "../../components/Q_A_Admin";

function FAQRequest() {
  const faqs_request = useSelector((state) => state.auth.faqs_request);
  const didOnce = React.useRef(false);
  const dispatch = useDispatch();
  useEffect(() => {
    if (!faqs_request && !didOnce.current) {
      didOnce.current = true;
      request_caller({
        method: "get",
        endpoint: "/faq/accept",
        data: {},
        successToast: false,
      })
        .then((res) => {
          dispatch(setFAQRequests(res.data));
        })
        .catch((_err) => {
          dispatch(setFAQRequests([]));
        });
    }
  }, [faqs_request]);

  return (
    <div className="">
      <NavBar />
      <div className="pt-4">
        {faqs_request && faqs_request.length === 0 && (
          <div className="text-center">No Requests found</div>
        )}
        {faqs_request && faqs_request.length !== 0 && (
          <div className="container">
            <div className="flex-row justify-content-between">
              <h2>Pending FAQ Requests</h2>
            </div>
            <Q_A_Admin />
          </div>
        )}
      </div>
    </div>
  );
}

export default FAQRequest;
