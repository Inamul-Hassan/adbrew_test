import './App.css';
import { useEffect, useState } from 'react';

export function App() {
  const [newTodo, setNewTodo] = useState("");
  const [todoList, setTodoList] = useState([]);
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:8000/todos/';

  // function to fetch todos from the server
  const fetchTodos = async () => {
    try {
      const response = await fetch(API_URL, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setTodoList(data);
    } catch (error) {
      setError(error.message);
      console.error('Fetch todos error:', error);
    }
  };

  // function to create a new todo  
  const createTodo = async (e) => {
    e.preventDefault();

    if (!newTodo.trim()) {
      setError("ToDo cannot be empty.");
      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ todo: newTodo }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      // clear the input field and fetch the updated list of todos
      setNewTodo("");
      fetchTodos();
    } catch (error) {
      setError(error.message);
      console.error('Create todo error:', error);
    }
  };

  // fetch todos only once when the app loads
  useEffect(() => {
    fetchTodos();
  }, []);


  return (
    <div className="App">
      <h1>List of TODOs</h1>
      {error && <p className="error">{error}</p>}
      <ul className='listItems'>
        {todoList.length > 0 ? (
          todoList.map((item) => (
            <li key={item._id}>{item.todo}</li>
          ))
        ) : (
          <p>No TODOs found.</p>
        )}
      </ul>
      <h1>Create a TODO</h1>
      <form onSubmit={createTodo}>
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
}

export default App;
