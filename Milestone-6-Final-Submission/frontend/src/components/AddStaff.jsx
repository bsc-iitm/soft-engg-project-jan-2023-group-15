import React from "react";
import { Button, Form, Modal, ModalBody, ModalHeader } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { FaPenAlt } from "react-icons/fa";
import request_caller from "../api/request.handler";
import { setStaffList } from "../store/auth/authSlice";

function AddStaff({ editQuery, staff }) {
  const [show, setShow] = React.useState(false);
  const user = useSelector((state) => state.auth.user);
  const staffList = useSelector((state) => state.auth.staffList);
  const dispatch = useDispatch();
  const submitForm = (e) => {
    e.preventDefault();
    const data = {
        email: e.target[0].value,
        username: e.target[1].value,
    }
    if (editQuery) {
      data.staff_id = staff.id;
    }
    request_caller({
      method: editQuery ? "put" : "post",
      endpoint: "/support_register",
      data,
      successToast: true,
    }).then((res) => {
      if (res.success) {
        if (editQuery) {
          const lc_staffList = [...staffList];
          const index = lc_staffList.findIndex((staff) => staff.id === res.data.id);
          if (index !== -1) {
            lc_staffList[index] = res.data;
            dispatch(setStaffList(lc_staffList));
          }
        } else {
          dispatch(setStaffList([res.data, ...staffList]));
        }
        setShow(false);
      }
    });
  };

  return (
    (user.role === "ADMIN") && (
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
              Add Staff
            </Button>
          </div>
        )}
        <Modal
          show={show}
          onHide={() => {
            setShow(false);
          }}
        >
          <ModalHeader>{editQuery ? "Edit" : "Create"} Staff</ModalHeader>
          <ModalBody>
            <Form onSubmit={submitForm}>
              <Form.Group>
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="Enter email"
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>Username</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter username"
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

export default AddStaff;
