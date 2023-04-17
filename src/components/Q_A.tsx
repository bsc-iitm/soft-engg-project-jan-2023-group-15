import React, { useState } from "react";
import "../styles/Q_A.css";

type Props = {
  questions: { question: string; answer: string }[];
};

const Q_A: React.FC<Props> = ({ questions }) => {
  const [selectedQuestionIndex, setSelectedQuestionIndex] = useState(-1);

  const handleQuestionClick = (index: number) => {
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
            <span>{q.question}</span>
            <div
              className={`faq-arrow ${
                index === selectedQuestionIndex ? "open" : ""
              }`}
            >
              <i className="fas fa-chevron-down"></i>
            </div>
          </div>
          <div
            className={`faq-answer ${
              index === selectedQuestionIndex ? "open" : ""
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