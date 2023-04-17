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

const AdminProfile: React.FC = () => {
    return (
      <div className="">
        <NavBar isAdmin home={"/option2"} faq={"/option2/FAQ"} profile={"/option2/profile"} staff={'/option2/staff'}/>
        <h2>Profile</h2>
        <div className='UserDetails'>
          <UserDetails {...userDetails}/>
        </div>
      </div>
    );
  };
  
export default AdminProfile;