const PRIORITY_STYLES = {
  0: 'bg-gray-100 text-gray-700',
  1: 'bg-yellow-100 text-yellow-800',
  2: 'bg-red-100 text-red-800',
};

const PRIORITY_LABELS = { 0: 'Low', 1: 'Medium', 2: 'High' };

export default function TodoCard({ todo, onDelete, onToggle, onPriorityChange }) {
  const isDone = todo.status === 'done';

  return (
    <div className={`flex items-center gap-3 rounded-lg border p-4 transition ${isDone ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-white'}`}>
      <button
        onClick={() => onToggle(todo.id)}
        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition ${isDone ? 'border-green-500 bg-green-500 text-white' : 'border-gray-300 hover:border-blue-400'}`}
      >
        {isDone && '✓'}
      </button>

      <div className="flex-1 min-w-0">
        <p className={`font-medium truncate ${isDone ? 'line-through text-gray-400' : 'text-gray-900'}`}>
          {todo.title}
        </p>
        {todo.due_date && (
          <p className="text-xs text-gray-500 mt-0.5">Due: {todo.due_date}</p>
        )}
      </div>

      <select
        value={todo.priority}
        onChange={(e) => onPriorityChange(todo.id, Number(e.target.value))}
        className={`rounded-full px-2 py-0.5 text-xs font-semibold ${PRIORITY_STYLES[todo.priority]}`}
      >
        {Object.entries(PRIORITY_LABELS).map(([val, label]) => (
          <option key={val} value={val}>{label}</option>
        ))}
      </select>

      <button
        onClick={() => onDelete(todo.id)}
        className="text-gray-400 hover:text-red-500 transition text-lg"
      >
        &times;
      </button>
    </div>
  );
}
