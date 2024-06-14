import React from 'react';
import TodoItem from './TodoItem';

const TodoList = ({ todoList, error }) => {
  return (
    <div>
      <h1>List of TODOs</h1>
      {error && <p className="error">{error}</p>}
      <ul className='listItems'>
        {todoList.length > 0 ? (
          todoList.map((item) => (
            <TodoItem key={item._id} item={item} />
          ))
        ) : (
          <p>No TODOs found.</p>
        )}
      </ul>
    </div>
  );
};

export default TodoList;
