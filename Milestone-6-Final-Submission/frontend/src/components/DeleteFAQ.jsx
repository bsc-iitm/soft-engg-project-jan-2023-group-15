import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { FaTrash } from "react-icons/fa";
import request_caller from "../api/request.handler";
import { setFAQs } from "../store/auth/authSlice";

function DeleteFAQ({ faq }) {
  const user = useSelector((state) => state.auth.user);
  const faqs = useSelector((state) => state.auth.faqs);
  const dispatch = useDispatch();
  const deleteFaq = () => {
    request_caller({
      method: "delete",
      endpoint: "/faq",
      data: { faq_id: faq.id },
      successToast: true,
    }).then((res) => {
      if (res.success) {
        const lc_faqs = [...faqs];
        const updated = lc_faqs.filter((lc) => lc.id !== faq.id);
        dispatch(setFAQs(updated));
      }
    });
  };
  return (
    user.role === "ADMIN" && (
      <>
        <button className="btn p-1" onClick={deleteFaq}>
          <FaTrash size={15} />
        </button>
      </>
    )
  );
}

export default DeleteFAQ;
