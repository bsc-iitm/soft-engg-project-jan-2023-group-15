import React, { useState } from "react";
import "../styles/Q_A.css";
import { FaChevronDown } from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import request_caller from "../api/request.handler";
import { setFAQRequests } from "../store/auth/authSlice";

const Q_A_Admin = () => {
  const questions = useSelector((state) => state.auth.faqs_request);
  const [selectedQuestionIndex, setSelectedQuestionIndex] = useState(-1);
  const dispatch = useDispatch();

  const handleQuestionClick = (index) => {
    setSelectedQuestionIndex(index === selectedQuestionIndex ? -1 : index);
  };

  const acceptFAQ = (status, question) => {
    request_caller({
      method:"post",
      endpoint:"/faq/accept",
      data:{
        faq_id:question.id,
        rejected:status
      },
      successToast:true
    }).then((_res)=>{
      const lc_questions = [...questions];
      if(status == 0){
        const updated = lc_questions.filter((lc) => lc.id !== question.id);
        dispatch(setFAQRequests(updated))
      }else{
        const index = lc_questions.findIndex((lc) => lc.id === question.id)
        if(index !== -1){
          lc_questions[index] = {...lc_questions[index]}
          lc_questions[index].status = "DELETED";
          dispatch(setFAQRequests(lc_questions))
        }
      }
    })
  }

  return (
    <div className="faq-container">
      {questions.map((q, index) => (
        <div key={index} className="faq-question-container">
          <div
            className="faq-question"
            onClick={() => handleQuestionClick(index)}
          >
            <span>{q.title}</span>
            <p>{q.status}</p>
            <div className="flex-row justify-content-between align-center" style={{gap:"10px"}}>
              <div
                className={`faq-arrow ${
                  index === selectedQuestionIndex ? "open" : ""
                }`}
              >
                <FaChevronDown size={20} />
              </div>
              {
                q.status === "REQUESTED" &&
                <button className="btn btn-danger" onClick={()=> acceptFAQ(1, q)}>Reject</button>
              }
              {
                (q.status === "DELETED" || q.status === "REQUESTED") &&
                <button className="btn btn-success" onClick={()=> acceptFAQ(0, q)}>Accept</button>
              }
            </div>
          </div>
          <div
            className={`faq-answer ${
              index === selectedQuestionIndex ? "open p-2 " : ""
            }`}
          >
            {q.answer}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Q_A_Admin;
