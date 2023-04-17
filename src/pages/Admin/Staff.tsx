import React from 'react';
import NavBar from '../../components/NavBar';
import '../../styles/Profile.css';
import StaffDisplay, {StaffProps} from '../../components/StaffDisplay';

const staffList: StaffProps[] = [
    {
      name: 'John Doe',
      position: 'Manager',
      photo: '/avatar.svg',
      email: 'john.doe@example.com',
      phone: '+1 (123) 456-7890'
    },
    {
      name: 'Jane Doe',
      position: 'Assistant Manager',
      photo: '/avatar.svg',
      email: 'jane.doe@example.com',
      phone: '+1 (123) 456-7890'
    },
    {
        name: 'John Doe',
        position: 'Manager',
        photo: '/avatar.svg',
        email: 'john.doe@example.com',
        phone: '+1 (123) 456-7890'
    },
    {
        name: 'Jane Doe',
        position: 'Assistant Manager',
        photo: '/avatar.svg',
        email: 'jane.doe@example.com',
        phone: '+1 (123) 456-7890'
    },
      {
        name: 'John Doe',
        position: 'Manager',
        photo: '/avatar.svg',
        email: 'john.doe@example.com',
        phone: '+1 (123) 456-7890'
      },
      {
        name: 'Jane Doe',
        position: 'Assistant Manager',
        photo: '/avatar.svg',
        email: 'jane.doe@example.com',
        phone: '+1 (123) 456-7890'
      },
      {
        name: 'John Doe',
        position: 'Manager',
        photo: '/avatar.svg',
        email: 'john.doe@example.com',
        phone: '+1 (123) 456-7890'
      },
      {
        name: 'Jane Doe',
        position: 'Assistant Manager',
        photo: '/avatar.svg',
        email: 'jane.doe@example.com',
        phone: '+1 (123) 456-7890'
      },
]

const Staff: React.FC = () => {
    return (
      <div className="">
        <NavBar isAdmin home={"/option2"} faq={"/option2/FAQ"} profile={"/option2/profile"} staff={'/option2/staff'}/>
        <StaffDisplay staffList={staffList} />
      </div>
    );
  };
  
export default Staff;