import React, { useState } from 'react';
import { Navbar, Container } from 'react-bootstrap';
import '../styles/Header.css';

interface Props {
    onSignInClick: any 
}

const Header: React.FC<Props> = () => {

  return (
    <>
      <Navbar className='nav' bg="light">
        <Container>
          <Navbar.Brand>
            <img className='img'
              alt="logo"
              src="/IITM.svg"
              width="40"
              height="40"
            />
            Support Ticket System
          </Navbar.Brand>
        </Container>
      </Navbar> 
    </>
  );
};

export default Header;