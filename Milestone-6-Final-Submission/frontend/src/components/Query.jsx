import React, { useState } from "react";
import "../styles/Query.css";
import request_caller from "../api/request.handler";
import { useSelector, useDispatch } from "react-redux";
import { setTickets } from "../store/auth/authSlice";
import { FaAngleDown, FaAngleUp, FaTrash, FaMapPin } from "react-icons/fa";
import NewTicket from "../pages/Student/NewTicket";
import ShowTicket from "./ShowTicket";
import Vote from "./Vote";

const Query = ({ queryList }) => {
  const [showAnswer, setShowAnswer] = useState(false);
  const tickets = useSelector((state) => state.auth.tickets);
  const user = useSelector((state) => state.auth.user);
  const dispatch = useDispatch();

  const handleToggleAnswer = () => {
    setShowAnswer(!showAnswer);
  };

  const deleteTicket = () => {
    request_caller({
      method: "delete",
      endpoint: "/ticket",
      data: {
        ticket_id: queryList.id,
      },
      successToast: true,
    }).then((_res) => {
      let lc_tickets = [...tickets];
      lc_tickets = lc_tickets.filter((ticket) => ticket.id != queryList.id);
      dispatch(setTickets(lc_tickets));
    });
  };

  return (
    <div className="query-container">
      <div className="query-header">
        <div className="query-topic text-left">
          <p className="font-weight-light text-xs">
            {new Date(queryList.created_at).toLocaleString()}
          </p>
          <ShowTicket queryList={queryList} />

          <p className="text-muted text-xs mt-2">
            Asked by{" "}
            {queryList.created_by_id === user.id
              ? "You"
              : queryList?.created_by_user?.username}
            &nbsp;({queryList.created_by_user?.role})
          </p>
        </div>
        <div className="query-upvote">
          <Vote queryList={queryList} />
        </div>
        <div>
          {queryList.created_by_id === user.id && (
            <NewTicket editQuery={true} ticket={queryList} />
          )}
          {queryList.created_by_id === user.id && (
            <button className="btn p-1" onClick={deleteTicket}>
              <FaTrash size={15} />
            </button>
          )}
          {queryList.priority === "HIGH" && <FaMapPin size={25} />}
          <button className="btn p-1" onClick={handleToggleAnswer}>
            {!showAnswer ? <FaAngleDown size={25} /> : <FaAngleUp size={25} />}
          </button>
        </div>
      </div>
      {showAnswer && (
        <div className="query-answer">
          <div className="query-answer-text">{queryList.description}</div>
        </div>
      )}
    </div>
  );
};

export default Query;
