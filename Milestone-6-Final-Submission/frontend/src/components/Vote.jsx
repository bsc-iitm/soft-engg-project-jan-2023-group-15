import React, { useState } from "react";
import request_caller from "../api/request.handler";
import { setSpecificTicket, setTickets } from "../store/auth/authSlice";
import { useDispatch, useSelector } from "react-redux";
import { FaThumbsUp } from "react-icons/fa";

function Vote({ queryList, isReply, reply = {} }) {
  const tickets = useSelector((state) => state.auth.tickets);
  const specificTicket = useSelector((state) => state.auth.specificTicket);

  const [upvoted, setUpvoted] = useState(false);
  const dispatch = useDispatch();
  const handleUpvote = () => {
    const data = {
      vote: upvoted ? -1 : 1,
    };
    if (isReply) {
      data.reply_id = reply.id;
    } else {
      data.ticket_id = queryList.id;
    }
    request_caller({
      method: "post",
      endpoint: "/ticket/vote",
      data,
      successToast: false,
    }).then((_res) => {
      if (!_res.data?.already_voted) {
        if (isReply) {
          const lc_specificTicket = { ...specificTicket };
          let count;
          console.log(reply.votes.upvotes)
          if (upvoted) {
            count = reply.votes.upvotes - 1;
          } else {
            count = reply.votes.upvotes + 1;
          }
          lc_specificTicket.replies = [...lc_specificTicket.replies];
          const index = lc_specificTicket.replies.findIndex(
            (lc) => lc.id === reply.id
          );
          if (index !== -1) {
            lc_specificTicket.replies[index] = {
              ...lc_specificTicket.replies[index],
            };
            lc_specificTicket.replies[index].votes = {
              ...lc_specificTicket.replies[index].votes,
              upvotes: count,
            };
            dispatch(setSpecificTicket(lc_specificTicket));
          }
        } else {
          const lc_tickets = [...tickets];
          const index = lc_tickets.findIndex(
            (ticket) => ticket.id === queryList.id
          );
          console.log("====================================");
          console.log(index);
          console.log("====================================");
          if (index !== -1) {
            let count;
            if (upvoted) {
              count = queryList.votes.upvotes - 1;
            } else {
              count = queryList.votes.upvotes + 1;
            }
            lc_tickets[index] = { ...lc_tickets[index] };
            console.log("====================================");
            console.log(count, lc_tickets[index]);
            console.log("====================================");
            lc_tickets[index].votes = {
              ...lc_tickets[index].votes,
              upvotes: count,
            };

            dispatch(setTickets(lc_tickets));
          }
        }
      }
      setUpvoted((val) => !val);
    });
  };
  return (
    <div className="flex-row align-center">
      <button
        className={`btn ${upvoted ? "text-primary" : "text-default"} p-1`}
        onClick={handleUpvote}
      >
        <FaThumbsUp size={20} />
      </button>
      <div className="mt-2 query-upvote-count">
        {isReply ? reply.votes?.upvotes : queryList?.votes?.upvotes}
      </div>
    </div>
  );
}

export default Vote;
