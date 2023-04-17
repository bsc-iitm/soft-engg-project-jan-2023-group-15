import React, { useState } from 'react';
import '../styles/Query.css';

export interface QueryProps {
    id: string;
    topic: string;
    query: string;
  }

interface query {
  queryList : QueryProps;
}

const Query: React.FC<query> = ({ queryList }) => {
    const [showAnswer, setShowAnswer] = useState(false);
    const [upvotes, setUpvotes] = useState(0);
  
    const handleUpvote = () => {
      setUpvotes(upvotes + 1);
    };
  
    const handleToggleAnswer = () => {
      setShowAnswer(!showAnswer);
    };
  
    return (
      <div className="query-container">
        <div className="query-header">
          <div className="query-id">{queryList.id}</div>
          <div className="query-topic">{queryList.topic}</div>
          <div className="query-upvote">
            <button onClick={handleUpvote}>
              <img
                src="./thumbsup.svg"
                height='20px'
                width='20px'
                alt="upvote"
                className="upvote-icon"
                style={{ filter: upvotes ? "brightness(0.5)" : "" }}
              />
            </button>
            <div className="query-upvote-count">{upvotes}</div>
          </div>
          <button className="query-arrow" onClick={handleToggleAnswer}>
            <img
              src="./down-arrow.svg"
              height='10px'
              width='10px'
              alt="down-arrow"
              className={`arrow-icon ${showAnswer ? "rotate" : ""}`}
            />
          </button>
        </div>
        {showAnswer && (
          <div className="query-answer">
            <div className="query-answer-text">{queryList.query}</div>
          </div>
        )}
      </div>
    );
};

export default Query;