import { request } from "./client";
import type { Metrics, Task, TaskCreate, TaskDetail, TaskFilters, TaskList } from "../types/task";

export const tasksApi = {
  list: (filters: TaskFilters = {}) => {
    const params = new URLSearchParams(
      Object.entries(filters).filter(([, v]) => v) as [string, string][],
    );
    return request<TaskList>(`/tasks?${params}`);
  },
  get: (id: string) => request<TaskDetail>(`/tasks/${id}`),
  create: (data: TaskCreate) =>
    request<Task>("/tasks", { method: "POST", body: JSON.stringify(data) }),
  remove: (id: string) => request<void>(`/tasks/${id}`, { method: "DELETE" }),
  process: (id: string) => request<Task>(`/tasks/${id}/process`, { method: "POST" }),
  retry: (id: string) => request<Task>(`/tasks/${id}/retry`, { method: "POST" }),
  metrics: () => request<Metrics>("/metrics"),
};
