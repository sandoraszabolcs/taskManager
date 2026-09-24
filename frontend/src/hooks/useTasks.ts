import { useCallback, useEffect, useState } from "react";
import { tasksApi } from "../api/tasks";
import type { Task, TaskFilters } from "../types/task";

// TODO: useTask, useMetrics, and polling for tasks in PENDING/PROCESSING state.

export function useTasks(filters: TaskFilters = {}) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Bumping this number re-runs the effect below; that's how reload() works.
  const [reloadKey, setReloadKey] = useState(0);

  const { status, search } = filters;

  useEffect(() => {
    // Set in cleanup so a slow response for old filters can't overwrite newer data.
    let cancelled = false;
    setLoading(true);
    setError(null);

    tasksApi
      .list({ status, search })
      .then((data) => {
        if (!cancelled) setTasks(data);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : String(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // Depend on primitives, not the filters object: a new object every render
    // would re-run this effect in an infinite loop.
  }, [status, search, reloadKey]);

  const reload = useCallback(() => setReloadKey((k) => k + 1), []);

  return { tasks, loading, error, reload };
}
