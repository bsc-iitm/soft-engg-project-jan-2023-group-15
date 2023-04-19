import React from 'react'
import request_caller from '../api/request.handler';
import { useSelector, useDispatch } from 'react-redux';
import { setSpecificTicket } from '../store/auth/authSlice';

const status = {
    "is_open":{
        0: "Open Ticket",
        1: "Close Ticket"
    },
    "is_offensive":{
        0: "Flag as offensive",
        1: "Unflag as offensive"
    },
    "is_answer":{
        0: "Mark as Solution",
        1: "Marked as Solution"
    }
}
const user_status = {
    "is_open":{
        0: "Closed Ticket",
    },
    "is_offensive":{
        1: "Flagged as offensive"
    },
    "is_answer":{
        1: "Marked as Solution"
    }
}
function StatusChange({ticket=true, status_type, status_id=0, reply}) {
    const specificTicket = useSelector((state) => state.auth.specificTicket);
    const user = useSelector((state) => state.auth.user);
    const dispatch = useDispatch();
    const statusUpdate = () => {
        console.log("Status Updated");
        const data = {}
        if(ticket){
            data.ticket_id = specificTicket.id
        }else{
            data.reply_id = reply.id
        }
        if(status_type === "is_open"){
            data.is_open = status_id === 0 ? 1 : 0
        }
        if(status_type === "is_offensive"){
            data.is_offensive = status_id === 0 ? 1 : 0
        }
        if(status_type === "is_answer"){
            data.is_answer = status_id === 0 ? 1 : 0
        }
        request_caller({
            method: "post",
            endpoint: "/ticket/status",
            data,
            successToast:true,
        }).then((res)=>{
            if(ticket){
                dispatch(setSpecificTicket(res.data))
            }else{
                const lc_specificTicket = { ...specificTicket };
                lc_specificTicket.replies = [...lc_specificTicket.replies];
                const index = lc_specificTicket.replies.findIndex(
                    (lc) => lc.id === reply.id
                );
                if (index !== -1) {
                    lc_specificTicket.replies[index] = res.data
                    dispatch(setSpecificTicket(lc_specificTicket));
                }
            }
        })
    }
  return (
    <>
        {
            user.role === 'STUDENT' ? 
            user_status?.[status_type]?.[status_id] &&
            <div className='bg-info px-4 py-2'>
                {user_status[status_type][status_id]}
            </div>
            :
            <button className="btn btn-outline-secondary" onClick={statusUpdate}>
                {status[status_type][status_id]}
            </button>
        }
    </>
  )
}

export default StatusChange