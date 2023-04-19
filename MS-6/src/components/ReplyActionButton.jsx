import React, { useState } from "react";
import { FaTrash, FaPenAlt } from "react-icons/fa";
import AddReply from "./AddReply";
import { Modal } from "react-bootstrap";
import { useSelector, useDispatch } from "react-redux";
import request_caller from "../api/request.handler";
import { setSpecificTicket } from "../store/auth/authSlice";

function ReplyActionButton({ reply }) {
  const [showModal, setShowModal] = useState(false);
  const user = useSelector((state) => state.auth.user);
  const specificTicket = useSelector((state) => state.auth.specificTicket);
  const dispatch = useDispatch();

  const deleteReply = () => {
    request_caller({
      method: "delete",
      endpoint: "/ticket/reply",
      data: {
        reply_id: reply.id,
      },
      successToast: true,
    }).then((res) => {
      if (res.success) {
        const lc_specificTicket = { ...specificTicket };
        lc_specificTicket.replies = lc_specificTicket.replies.filter(
          (a) => a.id !== reply.id
        );
        dispatch(setSpecificTicket(lc_specificTicket));
      }
    });
  };
  return (
    reply.created_by_user?.id === user.id && (
      <>
        <div className="flex-row mb-4 align-center">
          <button
            className="btn"
            onClick={() => {
              setShowModal(true);
            }}
          >
            <FaPenAlt size={25} />
          </button>
          <button className="btn" onClick={()=>deleteReply()}>
            <FaTrash size={25} />
          </button>
        </div>
        <Modal
          show={showModal}
          onHide={() => {
            setShowModal(false);
          }}
        >
          <Modal.Body>
            <AddReply
              editQuery={true}
              reply={reply}
              callback={() => {
                setShowModal(false);
              }}
            />
          </Modal.Body>
        </Modal>
      </>
    )
  );
}

export default ReplyActionButton;
