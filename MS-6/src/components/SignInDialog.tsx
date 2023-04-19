import React from "react";
import { Modal, Button } from "react-bootstrap";
import GoogleButton from "react-google-button";

interface SignInDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

const SignInDialog: React.FC<SignInDialogProps> = ({ isOpen, onClose }) => {
  const handleOption1Click = () => {
    window.location.href = "/option1";
  };

  const handleOption2Click = () => {
    window.location.href = "/option2";
  };

  const handleOption3Click = () => {
    window.location.href = "/option3";
  };

  return (
    <Modal show={isOpen} onHide={onClose}>
      <Modal.Header className="" closeButton>
        <GoogleButton
          onClick={() => {
            console.log("Google button clicked");
          }}
        />
      </Modal.Header>
      <Modal.Body>
        <Button variant="primary" onClick={handleOption1Click}>
          Option 1
        </Button>{" "}
        <Button variant="secondary" onClick={handleOption2Click}>
          Option 2
        </Button>{" "}
        <Button variant="success" onClick={handleOption3Click}>
          Option 3
        </Button>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default SignInDialog;
