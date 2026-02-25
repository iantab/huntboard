import { api } from "./axios";
import type { DashboardStats, ActivityStat } from "../types";

export const dashboardApi = {
  getStats: async () => {
    const response = await api.get<DashboardStats>("/api/v1/dashboard/stats/");
    return response.data;
  },

  getActivity: async () => {
    const response = await api.get<ActivityStat[]>(
      "/api/v1/dashboard/activity/",
    );
    return response.data;
  },
};
