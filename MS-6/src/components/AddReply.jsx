import React from "react";
import { Button, Form } from "react-bootstrap";
import { setSpecificTicket } from "../store/auth/authSlice";
import { useSelector, useDispatch } from "react-redux";
import request_caller from "../api/request.handler";

function AddReply({ editQuery, reply, callback=()=>{} }) {
  const specificTicket = useSelector((state) => state.auth.specificTicket);
  const dispatch = useDispatch();

  const submitReply = (e) => {
    e.preventDefault();
    const data = {
      reply: e.target[0].value,
    };
    if (editQuery) {
      data.reply_id = reply.id;
    } else {
      data.ticket_id = specificTicket.id;
    }
    request_caller({
      method: editQuery ? "put" : "post",
      endpoint: "/ticket/reply",
      data,
      successToast: true,
    }).then((res) => {
      if (res.success) {
        const lc_specificTicket = { ...specificTicket };
        if (editQuery) {
          lc_specificTicket.replies = lc_specificTicket.replies.filter(
            (a) => a.id !== reply.id
          );
        }
        lc_specificTicket.replies = [res.data, ...lc_specificTicket.replies];
        dispatch(setSpecificTicket(lc_specificTicket));
        e.target.reset();
        callback();
      }
    });
  };
  return (
    <>
      <Form onSubmit={submitReply}>
        <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
          <Form.Label>Reply</Form.Label>
          <Form.Control as="textarea" rows={3} defaultValue={reply?.reply} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Reply
        </Button>
      </Form>
    </>
  );
}

export default AddReply;
