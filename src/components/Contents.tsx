import React, { useState } from 'react';
import '../styles/Contents.css';
import SignInDialog from './SignInDialog';

interface Props {}

const Contents: React.FC<Props> = () => {

  const [isSignInOpen, setIsSignInOpen] = useState(false);

  const handleSignInClick = () => {
    setIsSignInOpen(true);
  };

  const handleCloseSignIn = () => {
    setIsSignInOpen(false);
  };


  return (
    <div className="contents">
      <img 
        width="350"
        height="350"  
        src="/IITM.svg" 
        alt="Big Logo" />
      <p>The Support Ticket System App to support the entire the Support Team</p>
      <button onClick={handleSignInClick}>Sign In</button>
      <SignInDialog isOpen={isSignInOpen} onClose={handleCloseSignIn} />
    </div>
  );
};

export default Contents;
