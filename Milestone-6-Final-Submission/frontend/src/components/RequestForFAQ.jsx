import React from "react";
import request_caller from "../api/request.handler";
import { useSelector } from "react-redux";

function RequestForFAQ({ ticket }) {
  const user = useSelector((state) => state.auth.user);
  const requestForFAQHandler = () => {
    request_caller({
      method: "post",
      endpoint: "/faq/request",
      data: {
        ticket_id: ticket.id,
      },
      successToast: true,
    }).then((res) => {
      console.log(res);
    });
  };
  return (
    user.role === "SUPPORT_STAFF" && (
      <>
        <button
          className="btn btn-outline-secondary"
          onClick={requestForFAQHandler}
        >
          Request for FAQ
        </button>
      </>
    )
  );
}

export default RequestForFAQ;
