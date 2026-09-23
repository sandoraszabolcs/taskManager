export type TaskStatus = "PENDING" | "PROCESSING" | "COMPLETED" | "FAILED";

export type TaskEventType =
  | "CREATED"
  | "PROCESSING_STARTED"
  | "COMPLETED"
  | "FAILED"
  | "RETRIED";

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  retry_count: number;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskEvent {
  id: number;
  event_type: TaskEventType;
  created_at: string;
  metadata: Record<string, unknown> | null;
}

export interface TaskDetail extends Task {
  events: TaskEvent[];
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskFilters {
  status?: TaskStatus;
  search?: string;
}

export interface TaskList {
  items: Task[];
  total: number;
}

export interface Metrics {
  total: number;
  by_status: Record<TaskStatus, number>;
  queue_length: number;
}
