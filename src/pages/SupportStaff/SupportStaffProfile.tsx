import React from 'react';
import NavBar from '../../components/NavBar';
import UserDetails from '../../components/UserDetails';
import '../../styles/Profile.css';

const userDetails = {
  avatar: '/avatar.svg' ,
  name: "John Doe",
  email: "john.doe@example.com",
  type: "Premium User",
  joiningDate: "20/05/2003",
};

const SupportStaffProfile: React.FC = () => {
    return (
      <div className="">
        <NavBar home={"/option3"} faq={"/option3/FAQ"} profile={"/option3/profile"} staff={''}/>
        <h2>Profile</h2>
        <div className='UserDetails'>
          <UserDetails {...userDetails}/>
        </div>
      </div>
    );
  };
  
export default SupportStaffProfile;