import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/NavBar.css';

interface Links {
  home: string,
  faq : string,
  profile: string,
  staff: string,
  isAdmin?: boolean
}

const NavBar: React.FC<Links> = ({ isAdmin = false, home, faq, profile, staff}) => {
  return (
    <nav className="Navbar">
      <div className="Navbar-container">
        <div className="Navbar-buttons">
          <img height='30px' width='30px' src={'/IITM.svg'} className="Navbar-logo" alt="Logo" />
          <Link to="/" className="Navbar-appname">
            Support Ticket System
          </Link>
          <Link to={home} className="Navbar-homebutton">
            Home
          </Link>
          <Link to={faq} className="Navbar-faqbutton">
            FAQs
          </Link>
          {isAdmin && <Link to={staff} className="Navbar-faqbutton">
            Staff
          </Link>}
          <Link to={profile} className="Navbar-avatarbutton">
            <button className="Navbar-avatarbutton">
              <img src={'/user.svg'} height='30px' width='30px' alt="User Avatar" />
            </button>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;