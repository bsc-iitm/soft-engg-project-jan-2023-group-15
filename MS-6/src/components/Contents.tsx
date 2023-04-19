import React, { useState } from "react";
import "../styles/Contents.css";
import GoogleButton from "react-google-button";
import { googleAuthHandler } from "../utility/google";

interface Props {}

const Contents: React.FC<Props> = () => {
  const [isStaff, setIsStaff] = useState(false);

  return (
    <div className="contents">
      <img width="350" height="350" src="/IITM.svg" alt="Big Logo" />
      <p>
        The Support Ticket System App to support the entire the Support Team
      </p>
      <GoogleButton
        onClick={() => {
          googleAuthHandler(isStaff);
        }}
      />
      <a
        href="#!"
        onClick={(e) => {
          e.preventDefault();
          setIsStaff(!isStaff);
        }}
      >
        Sign in as {isStaff ? "student" : "staff"}?
      </a>
    </div>
  );
};

export default Contents;
