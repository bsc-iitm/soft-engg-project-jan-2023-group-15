import React from 'react';
import NavBar from '../../components/NavBar';
import Query, {QueryProps} from '../../components/Query';

const queries: QueryProps[] = [
  {
    id: 'AA101',
    topic: "How to use the Query component?",
    query: "I want to learn how to use the Query component in my React application. Can you please provide an example?",
  },
  {
    id: 'AA102',
    topic: "How to style the Query component?",
    query: "I want to change the font size and color of the text in the Query component. How can I do that?",
  },
  {
    id: 'AA101',
    topic: "How to use the Query component?",
    query: "I want to learn how to use the Query component in my React application. Can you please provide an example?",
  },
  {
    id: 'AA102',
    topic: "How to style the Query component?",
    query: "I want to change the font size and color of the text in the Query component. How can I do that?",
  },
  // ... other queries
];

const Option2: React.FC = () => {
  return (
    <div>
      <NavBar isAdmin home={"/option2"} faq={"/option2/FAQ"} profile={"/option2/profile"} staff={'/option2/staff'}/>
      {/* {queries.map((query) => {
        <Query 
          key={query.id}
          id={query.id}
          topic={query.topic}
          query={query.query}
      })} */}
      <div className=''>
        {queries.map((query) => (
          <Query key={query.id} queryList={query} />
        ))}
      </div>
    </div>
  );
};

export default Option2;
