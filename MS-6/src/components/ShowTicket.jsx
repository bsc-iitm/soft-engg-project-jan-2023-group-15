import React from "react";
import request_caller from "../api/request.handler";
import { useSelector, useDispatch } from "react-redux";
import { setSpecificTicket } from "../store/auth/authSlice";
import { Button, Modal } from "react-bootstrap";
import Vote from "./Vote";
import StatusChange from "./StatusChange";
import RequestForFAQ from "./RequestForFAQ";
import PinTicket from "./PinTicket";
import ReplyActionButton from "./ReplyActionButton";
import AddReply from "./AddReply";
import BlockUser from "./BlockUser";

function ShowTicket({ queryList }) {
  const [showDetails, setShowDetails] = React.useState(false);
  const specificTicket = useSelector((state) => state.auth.specificTicket);
  const dispatch = useDispatch();
  const get_ticket_details = () => {
    if (specificTicket.id === queryList.id) {
      setShowDetails(true);
      return;
    }
    request_caller({
      method: "get",
      endpoint: `/ticket`,
      data: {
        ticket_id: queryList.id,
      },
    }).then((res) => {
      dispatch(setSpecificTicket(res.data));
      setShowDetails(true);
    });
  };

  return (
    <>
      <a
        href="#!"
        onClick={(e) => {
          e.preventDefault();
          get_ticket_details();
        }}
      >
        {queryList.title}
      </a>
      <Modal
        size="lg"
        show={showDetails}
        onHide={() => {
          setShowDetails(false);
        }}
      >
        <Modal.Header closeButton>
          <Modal.Title>#{specificTicket.id}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="row">
            <div className="col-12 flex-row mb-4 align-center">
              <img
                style={{ width: "40px", height: "40px" }}
                src={specificTicket.created_by_user?.profile_picture}
                alt=""
                className="rounded-circle mr-2"
              />
              <p>{specificTicket.created_by_user?.username}</p>
            </div>
          </div>
          <div className="row">
            <div className="col-12">
              <h5>{specificTicket.title}</h5>
            </div>
            <div className="col-12">
              <p>{specificTicket.description}</p>
            </div>
            <div className="col-12 flex-row justify-content-between">
              <Vote queryList={queryList} />
              <p className="text-muted mb-0 flex-row align-center">
                {new Date(specificTicket.created_at).toLocaleString()}
              </p>
            </div>
            <div className="col-12 flex-row justify-content-between mt-4">
              <StatusChange
                status_type="is_offensive"
                status_id={specificTicket.is_offensive ? 1 : 0}
              />
              <StatusChange
                status_type="is_open"
                status_id={specificTicket.is_open ? 1 : 0}
              />
              <RequestForFAQ ticket={specificTicket} />
              <PinTicket ticket={specificTicket} />
              <BlockUser user={specificTicket.created_by_user} />
            </div>
          </div>

          <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-1 border-bottom"></div>
        <AddReply />
          {specificTicket.replies && specificTicket.replies.length > 0 && (
            <div className="row">
              <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-1 border-bottom"></div>

              <div className="col-12">
                <h5>Replies</h5>
              </div>
              {specificTicket.replies.map((reply) => (
                <div className="col-12 my-1" key={reply.id}>
                  <div className="card">
                    <div className="card-body">
                      <div className="col-12">
                        <div
                          className="flex-row justify-content-between"
                          style={{ width: "100%" }}
                        >
                          <div className="flex-row mb-4 align-center">
                            <img
                              style={{ width: "40px", height: "40px" }}
                              src={reply.created_by_user?.profile_picture}
                              alt=""
                              className="rounded-circle"
                            />
                            <p className="mb-0 mx-2">
                              {reply.created_by_user?.username}&nbsp;(
                              {reply.created_by_user?.role})
                            </p>
                          </div>
                          <ReplyActionButton reply={reply} />
                        </div>
                      </div>
                      <p>{reply.reply}</p>
                      <div className="col-12 flex-row justify-content-between">
                        <Vote
                          queryList={queryList}
                          reply={reply}
                          isReply={true}
                        />
                        <p className="text-muted mb-0 flex-row align-center">
                          {new Date(reply.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div className="col-12 flex-row justify-content-between">
                        <StatusChange
                          status_type="is_offensive"
                          status_id={reply.is_offensive ? 1 : 0}
                          ticket={false}
                          reply={reply}
                        />
                        <StatusChange
                          status_type="is_answer"
                          status_id={reply.is_answer ? 1 : 0}
                          ticket={false}
                          reply={reply}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="secondary"
            onClick={() => {
              setShowDetails(false);
            }}
          >
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default ShowTicket;
