import React from "react";
import request_caller from "../api/request.handler";
import { useSelector, useDispatch } from "react-redux";
import { setSpecificTicket, setTickets } from "../store/auth/authSlice";

function PinTicket({ ticket }) {
  const user = useSelector((state) => state.auth.user);
  const specificTicket = useSelector((state) => state.auth.specificTicket);
  const tickets = useSelector((state) => state.auth.tickets);
  const dispatch = useDispatch();
  const pinTicketHandler = () => {

    request_caller({
      method: "post",
      endpoint: "/ticket/pin",
      data: {
        ticket_id: ticket.id,
        pin: ticket.priority === "HIGH" ? 0 : 1,
      },
      successToast: true,
    }).then((_res) => {
        const lc_tickets = [...tickets];
        const index = lc_tickets.findIndex((t) => t.id === ticket.id);
        if (index !== -1) {
            lc_tickets[index] = {...lc_tickets[index]}
            lc_tickets[index].priority = ticket.priority === "HIGH" ? "LOW" : "HIGH"
            dispatch(setTickets(lc_tickets));
        }
        const lc_specificTicket = {...specificTicket};
        lc_specificTicket.priority = ticket.priority === "HIGH" ? "LOW" : "HIGH";
        dispatch(setSpecificTicket(lc_specificTicket));
    });
  };
  return (
    (user.role === "SUPPORT_STAFF" || user.role == "ADMIN") && (
      <>
        <button
          className="btn btn-outline-secondary"
          onClick={pinTicketHandler}
        >
          {ticket.priority === "HIGH" ? "Unpin" : "Pin"} Ticket
        </button>
      </>
    )
  );
}

export default PinTicket;
