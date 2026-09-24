import { Link } from "react-router-dom";
import StatusBadge from "../components/StatusBadge";
import { useTasks } from "../hooks/useTasks";

// TODO: TaskForm + TaskFilters above the table
export default function TaskListPage() {
  const { tasks, loading, error, reload } = useTasks();

  return (
    <main>
      <h1>Tasks</h1>
      <button onClick={reload} disabled={loading}>
        Refresh
      </button>

      {error && <p role="alert">Could not load tasks: {error}</p>}

      {loading && tasks.length === 0 ? (
        <p>Loading…</p>
      ) : tasks.length === 0 ? (
        <p>No tasks yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Status</th>
              <th>Retries</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((t) => (
              <tr key={t.id}>
                <td>
                  <Link to={`/tasks/${t.id}`}>{t.title}</Link>
                </td>
                <td>
                  <StatusBadge status={t.status} />
                </td>
                <td>{t.retry_count}</td>
                <td>{new Date(t.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
