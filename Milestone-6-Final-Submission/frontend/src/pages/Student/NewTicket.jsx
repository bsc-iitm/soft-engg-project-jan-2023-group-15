import React from "react";
import { Button, Form, Modal, ModalBody, ModalHeader } from "react-bootstrap";
import request_caller from "../../api/request.handler";
import { setTickets } from "../../store/auth/authSlice";
import { useDispatch, useSelector } from "react-redux";
import { FaPenAlt } from "react-icons/fa";

function NewTicket({ editQuery, ticket }) {
  const [show, setShow] = React.useState(false);
  const tickets = useSelector((state) => state.auth.tickets);
  const dispatch = useDispatch();
  const submitForm = (e) => {
    e.preventDefault();
    const data = {
      title: e.target[0].value,
      description: e.target[1].value,
    };
    if (editQuery) {
      data.ticket_id = ticket.id;
    }
    request_caller({
      method: editQuery ? "put" : "post",
      endpoint: "/ticket",
      data,
      successToast: true,
    }).then((res) => {
      if (res.success) {
        if (editQuery) {
          const lc_tickets = [...tickets];
          const index = lc_tickets.findIndex(
            (ticket) => ticket.id === res.data.id
          );
          if (index !== -1) {
            lc_tickets[index] = res.data;
            dispatch(setTickets(lc_tickets));
          }
        } else {
          dispatch(setTickets([res.data, ...tickets]));
        }
        setShow(false);
      }
    });
  };

  return (
    <>
      {editQuery ? (
        <button className="btn text-primary p-1" onClick={() => setShow(true)}>
          <FaPenAlt size={15} />
        </button>
      ) : (
        <div className=" position-fixed fixed-bottom p-2">
          <Button
            onClick={() => {
              setShow(true);
            }}
            className="btn btn-primary "
          >
            Create Ticket
          </Button>
        </div>
      )}
      <Modal
        show={show}
        onHide={() => {
          setShow(false);
        }}
      >
        <ModalHeader>{editQuery ? "Edit" : "Create"} ticket</ModalHeader>
        <ModalBody>
          <Form onSubmit={submitForm}>
            <Form.Group>
              <Form.Label>Subject</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter subject"
                defaultValue={ticket?.title}
              />
            </Form.Group>
            <Form.Group>
              <Form.Label>Message</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                defaultValue={ticket?.description}
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="mt-3">
              Submit
            </Button>
          </Form>
        </ModalBody>
      </Modal>
    </>
  );
}

export default NewTicket;
