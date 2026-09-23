import type { TaskStatus } from "../types/task";

export default function StatusBadge({ status }: { status: TaskStatus }) {
  // TODO: color per status
  return <span className={`badge badge-${status.toLowerCase()}`}>{status}</span>;
}
