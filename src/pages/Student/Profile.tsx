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

const Profile: React.FC = () => {
    return (
      <div className="">
        <NavBar home={"/option1"} faq={"/option1/FAQ"} profile={"/option1/profile"} staff={''} />
        <h2>Profile</h2>
        <div className='UserDetails'>
          <UserDetails {...userDetails}/>
        </div>
      </div>
    );
  };
  
export default Profile;