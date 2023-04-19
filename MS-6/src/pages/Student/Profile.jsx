import React from 'react';
import NavBar from '../../components/NavBar';
import UserDetails from '../../components/UserDetails';
import '../../styles/Profile.css';
import UnblockUserList from '../../components/UnblockUserList';


const Profile = () => {
    return (
      <div className="">
        <NavBar />
        <h2>Profile</h2>
        <div className='UserDetails'>
          <UserDetails />
          <UnblockUserList />
        </div>
      </div>
    );
  };
  
export default Profile;