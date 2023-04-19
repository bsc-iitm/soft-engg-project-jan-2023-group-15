import React, { useState } from 'react';
import Header from '../components/Header';
import Contents from '../components/Contents';
import SignInDialog from '../components/SignInDialog';
import { Props } from 'react-modal';

const HomePage: React.FC = () => {
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    const handleSignInClick = () => {
      setIsDialogOpen(true);
    };
  
    const handleDialogClose = () => {
      setIsDialogOpen(false);
    };

    return (
        <div>
            <Header onSignInClick={handleSignInClick} />
            <Contents />
            <SignInDialog isOpen={isDialogOpen} onClose={handleDialogClose} />
        </div>
    );
};

export default HomePage;