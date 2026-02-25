import { api } from "./axios";
import type { User, TokenPair } from "../types";

export const authApi = {
  register: async (data: Record<string, string>) => {
    const response = await api.post<User>("/api/v1/auth/register/", data);
    return response.data;
  },

  login: async (data: Record<string, string>) => {
    const response = await api.post<TokenPair>("/api/v1/auth/token/", data);
    return response.data;
  },

  refresh: async (refresh: string) => {
    const response = await api.post<{ access: string }>(
      "/api/v1/auth/token/refresh/",
      { refresh },
    );
    return response.data;
  },

  getMe: async () => {
    const response = await api.get<User>("/api/v1/auth/me/");
    return response.data;
  },

  updateMe: async (data: Partial<User>) => {
    const response = await api.patch<User>("/api/v1/auth/me/", data);
    return response.data;
  },
};
