import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getTodos, createTodo, deleteTodo, toggleTodo, updateTodo } from '../api/todos';
import TodoCard from '../components/TodoCard';
import AddTodoForm from '../components/AddTodoForm';

export default function TodoPage() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const { data } = await getTodos();
      setTodos(data);
    } catch {
      // 401 handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = async (todoData) => {
    const { data } = await createTodo(todoData);
    setTodos((prev) => [data, ...prev]);
  };

  const handleDelete = async (id) => {
    await deleteTodo(id);
    setTodos((prev) => prev.filter((t) => t.id !== id));
  };

  const handleToggle = async (id) => {
    const { data } = await toggleTodo(id);
    setTodos((prev) => prev.map((t) => (t.id === id ? data : t)));
  };

  const handlePriorityChange = async (id, priority) => {
    const { data } = await updateTodo(id, { priority });
    setTodos((prev) => prev.map((t) => (t.id === id ? data : t)));
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  const pending = todos.filter((t) => t.status !== 'done');
  const done = todos.filter((t) => t.status === 'done');

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b bg-white px-6 py-4">
        <div className="mx-auto flex max-w-2xl items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900">My Todos</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-500">{user?.email}</span>
            <button onClick={handleLogout} className="text-sm text-red-500 hover:underline">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-2xl px-6 py-8">
        <AddTodoForm onAdd={handleAdd} />

        {todos.length === 0 ? (
          <p className="text-center text-gray-400 py-12">No todos yet. Add one above!</p>
        ) : (
          <div className="space-y-3">
            {pending.map((todo) => (
              <TodoCard
                key={todo.id}
                todo={todo}
                onDelete={handleDelete}
                onToggle={handleToggle}
                onPriorityChange={handlePriorityChange}
              />
            ))}
            {done.length > 0 && (
              <>
                <h2 className="pt-4 text-sm font-semibold text-gray-400 uppercase tracking-wider">
                  Completed ({done.length})
                </h2>
                {done.map((todo) => (
                  <TodoCard
                    key={todo.id}
                    todo={todo}
                    onDelete={handleDelete}
                    onToggle={handleToggle}
                    onPriorityChange={handlePriorityChange}
                  />
                ))}
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
