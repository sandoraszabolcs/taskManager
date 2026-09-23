import { Link, Route, Routes } from "react-router-dom";
import TaskListPage from "./pages/TaskListPage";
import TaskDetailPage from "./pages/TaskDetailPage";
import MetricsPage from "./pages/MetricsPage";

export default function App() {
  return (
    <>
      <nav>
        <Link to="/">Tasks</Link> | <Link to="/metrics">Metrics</Link>
      </nav>
      <Routes>
        <Route path="/" element={<TaskListPage />} />
        <Route path="/tasks/:id" element={<TaskDetailPage />} />
        <Route path="/metrics" element={<MetricsPage />} />
      </Routes>
    </>
  );
}
