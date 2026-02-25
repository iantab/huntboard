import { api } from "./axios";
import type {
  Application,
  Contact,
  Interview,
  StatusHistory,
  PaginatedResponse,
} from "../types";

export const applicationsApi = {
  list: async (params?: Record<string, string | number>) => {
    const response = await api.get<PaginatedResponse<Application>>(
      "/api/v1/applications/",
      { params },
    );
    return response.data;
  },

  get: async (id: string) => {
    const response = await api.get<Application>(`/api/v1/applications/${id}/`);
    return response.data;
  },

  create: async (data: Partial<Application>) => {
    const response = await api.post<Application>("/api/v1/applications/", data);
    return response.data;
  },

  update: async (id: string, data: Partial<Application>) => {
    const response = await api.patch<Application>(
      `/api/v1/applications/${id}/`,
      data,
    );
    return response.data;
  },

  delete: async (id: string) => {
    await api.delete(`/api/v1/applications/${id}/`);
  },

  advance: async (id: string) => {
    const response = await api.post<Application>(
      `/api/v1/applications/${id}/advance/`,
    );
    return response.data;
  },

  getHistory: async (id: string) => {
    const response = await api.get<StatusHistory[]>(
      `/api/v1/applications/${id}/history/`,
    );
    return response.data;
  },

  // Contacts
  listContacts: async (appId: string) => {
    const response = await api.get<Contact[]>(
      `/api/v1/applications/${appId}/contacts/`,
    );
    return response.data;
  },
  addContact: async (appId: string, data: Partial<Contact>) => {
    const response = await api.post<Contact>(
      `/api/v1/applications/${appId}/contacts/`,
      data,
    );
    return response.data;
  },
  updateContact: async (
    appId: string,
    contactId: string,
    data: Partial<Contact>,
  ) => {
    const response = await api.put<Contact>(
      `/api/v1/applications/${appId}/contacts/${contactId}/`,
      data,
    );
    return response.data;
  },
  deleteContact: async (appId: string, contactId: string) => {
    await api.delete(`/api/v1/applications/${appId}/contacts/${contactId}/`);
  },

  // Interviews
  listInterviews: async (appId: string) => {
    const response = await api.get<Interview[]>(
      `/api/v1/applications/${appId}/interviews/`,
    );
    return response.data;
  },
  addInterview: async (appId: string, data: Partial<Interview>) => {
    const response = await api.post<Interview>(
      `/api/v1/applications/${appId}/interviews/`,
      data,
    );
    return response.data;
  },
  updateInterview: async (
    appId: string,
    interviewId: string,
    data: Partial<Interview>,
  ) => {
    const response = await api.put<Interview>(
      `/api/v1/applications/${appId}/interviews/${interviewId}/`,
      data,
    );
    return response.data;
  },
  deleteInterview: async (appId: string, interviewId: string) => {
    await api.delete(
      `/api/v1/applications/${appId}/interviews/${interviewId}/`,
    );
  },
};
