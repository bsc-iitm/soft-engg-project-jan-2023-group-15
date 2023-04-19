import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import NavBar from "../../components/NavBar";
import Query from "../../components/Query";
import request_caller from "../../api/request.handler";
import { setTickets } from "../../store/auth/authSlice";
import NewTicket from "./NewTicket";

const Option1 = () => {
  const tickets = useSelector((state) => state.auth.tickets);
  const didOnce = React.useRef(false);
  const dispatch = useDispatch();
  useEffect(() => {
    if (!tickets && !didOnce.current) {
      didOnce.current = true;
      request_caller({
        method: "post",
        endpoint: "/ticket/all",
        data: {},
        successToast: false,
      })
        .then((res) => {
          dispatch(setTickets(res.data));
        })
        .catch((_err) => {
          dispatch(setTickets([]));
        });
    }
  }, [tickets]);

  return (
    <div>
      <NavBar home={"/"} faq={"/FAQ"} profile={"/profile"} staff={""} />
      <div className="pb-5 pt-3">
        {tickets &&
          tickets.map((query) => <Query key={query.id} queryList={query} />)}
        {tickets && tickets.length === 0 && (
          <div className="text-center">No tickets found</div>
        )}
      </div>
      <NewTicket />
    </div>
  );
};

export default Option1;
