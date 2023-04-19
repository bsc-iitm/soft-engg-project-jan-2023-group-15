import React, { useMemo } from 'react';
import { Link } from 'react-router-dom';
import '../styles/NavBar.css';
import { useSelector } from 'react-redux';

const NavBar = () => {
  const user = useSelector((state) => state.auth.user);
  const isAdmin = useMemo(() => user.role === "ADMIN", [user])
  return (
    <nav className="Navbar">
      <div className="Navbar-container">
        <div className="Navbar-buttons">
          <img height='30px' width='30px' src={'/IITM.svg'} className="Navbar-logo" alt="Logo" />
          <Link to="/" className="Navbar-appname">
            Support Ticket System
          </Link>
          <Link to="/" className="Navbar-homebutton">
            Home
          </Link>
          <Link to="/faq" className="Navbar-faqbutton">
            FAQs
          </Link>
          {isAdmin && <Link to="/staff" className="Navbar-faqbutton">
            Staff
          </Link>}
          <Link to="/profile" className="Navbar-avatarbutton">
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