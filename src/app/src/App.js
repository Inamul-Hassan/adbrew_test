import './App.css';
import { useEffect, useState } from 'react';
import TodoList from './components/TodoList';
import TodoForm from './components/TodoForm';
import { fetchTodos, createTodo } from './services/todoService';

export function App() {
  const [todoList, setTodoList] = useState([]);
  const [error, setError] = useState(null);

  // function to load todos from the server
  const loadTodos = async () => {
    try {
      const data = await fetchTodos();
      setTodoList(data);
    } catch (error) {
      setError(error.message);
      console.error('Fetch todos error:', error);
    }
  };

  // function to handle creating a new todo
  const handleCreateTodo = async (todo) => {
    if (!todo.trim()) {
      setError("ToDo cannot be empty.");
      return;
    }

    try {
      await createTodo(todo);
      loadTodos();
    } catch (error) {
      setError(error.message);
      console.error('Create todo error:', error);
    }
  };

  // fetch todos only once when the app loads
  useEffect(() => {
    loadTodos();
  }, []);

  return (
    <div className="App">
      <TodoList todoList={todoList} error={error} />
      <TodoForm createTodo={handleCreateTodo} />
    </div>
  );
}

export default App;
