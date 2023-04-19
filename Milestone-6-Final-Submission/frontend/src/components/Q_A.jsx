import React, { useState } from "react";
import "../styles/Q_A.css";
import { FaChevronDown } from "react-icons/fa";
import AddFAQ from "./AddFAQ";
import DeleteFAQ from "./DeleteFAQ";
import { useSelector } from "react-redux";

const Q_A = () => {
  const questions = useSelector((state) => state.auth.faqs);
  const [selectedQuestionIndex, setSelectedQuestionIndex] = useState(-1);

  const handleQuestionClick = (index) => {
    setSelectedQuestionIndex(index === selectedQuestionIndex ? -1 : index);
  };

  return (
    <div className="faq-container">
      {questions.map((q, index) => (
        <div key={index} className="faq-question-container">
          <div
            className="faq-question"
            onClick={() => handleQuestionClick(index)}
          >
            <span>{q.title}</span>
            <div className="flex-row justify-content-between align-center">
              
            <div
              className={`faq-arrow ${
                index === selectedQuestionIndex ? "open" : ""
              }`}
            >
              <FaChevronDown size={20} />
            </div>

            <AddFAQ editQuery={true} faq={q} />
            <DeleteFAQ faq={q} />
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

export default Q_A;
