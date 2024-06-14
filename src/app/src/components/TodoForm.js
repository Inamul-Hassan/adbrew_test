import React, { useState } from 'react';

const TodoForm = ({ createTodo }) => {
  const [newTodo, setNewTodo] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    createTodo(newTodo);
    setNewTodo("");
  };

  return (
    <div>
      <h1>Create a TODO</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="todo">TODO: </label>
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            required
          />
        </div>
        <div>
          <button type="submit">Add TODO</button>
        </div>
      </form>
    </div>
  );
};

export default TodoForm;
