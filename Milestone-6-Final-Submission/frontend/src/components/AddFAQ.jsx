import React from "react";
import { Button, Form, Modal, ModalBody, ModalHeader } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { FaPenAlt } from "react-icons/fa";
import request_caller from "../api/request.handler";
import { setFAQs } from "../store/auth/authSlice";

function AddFAQ({ editQuery, faq }) {
  const [show, setShow] = React.useState(false);
  const user = useSelector((state) => state.auth.user);
  const faqs = useSelector((state) => state.auth.faqs);
  const dispatch = useDispatch();
  const submitForm = (e) => {
    e.preventDefault();
    const data = {
      title: e.target[0].value,
      answer: e.target[1].value,
    };
    if (editQuery) {
      data.faq_id = faq.id;
    }
    request_caller({
      method: editQuery ? "put" : "post",
      endpoint: "/faq",
      data,
      successToast: true,
    }).then((res) => {
      if (res.success) {
        if (editQuery) {
          const lc_faqs = [...faqs];
          const index = lc_faqs.findIndex((faq) => faq.id === res.data.id);
          if (index !== -1) {
            lc_faqs[index] = res.data;
            dispatch(setFAQs(lc_faqs));
          }
        } else {
          dispatch(setFAQs([res.data, ...faqs]));
        }
        setShow(false);
      }
    });
  };

  return (
    //Support staff can edit the faq
    (user.role === "ADMIN" || (editQuery && user.role === "SUPPORT_STAFF")) && (
      <>
        {editQuery ? (
          <button
            className="btn text-primary p-1"
            onClick={() => setShow(true)}
          >
            <FaPenAlt size={15} />
          </button>
        ) : (
          <div className="p-2">
            <Button
              onClick={() => {
                setShow(true);
              }}
              className="btn btn-primary "
            >
              Create FAQ
            </Button>
          </div>
        )}
        <Modal
          show={show}
          onHide={() => {
            setShow(false);
          }}
        >
          <ModalHeader>{editQuery ? "Edit" : "Create"} FAQ</ModalHeader>
          <ModalBody>
            <Form onSubmit={submitForm}>
              <Form.Group>
                <Form.Label>Title</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter subject"
                  defaultValue={faq?.title}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>Answer</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  defaultValue={faq?.answer}
                />
              </Form.Group>
              <Button variant="primary" type="submit" className="mt-3">
                Submit
              </Button>
            </Form>
          </ModalBody>
        </Modal>
      </>
    )
  );
}

export default AddFAQ;
