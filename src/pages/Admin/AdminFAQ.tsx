import React from 'react';
import '../../styles/Contents.css';
import Q_A from '../../components/Q_A';
import NavBar from '../../components/NavBar';

const questions = [
  {
    question: "What is React?",
    answer: "React is a JavaScript library for building user interfaces.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
  {
    question: "What are the features of React?",
    answer:
      "Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow. Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.Some of the key features of React are virtual DOM, component-based architecture, JSX syntax, and uni-directional data flow.",
  },
];

const AdminFAQ: React.FC = () => {
  return (
    <div className="FAQ">
      <NavBar isAdmin home={"/option2"} faq={"/option2/FAQ"} profile={"/option2/profile"} staff={'/option2/staff'} />
      <h2>Frequently Asked Questions</h2>
      <Q_A questions={questions}/>
    </div>
  );
};

export default AdminFAQ;