import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { applicationsApi } from "../api/applications";
import type {
  Application,
  ApplicationStatus,
  PaginatedResponse,
} from "../types";

export function useCreateApplication() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<Application>) => applicationsApi.create(data),
    onSettled: () => {
      queryClient.refetchQueries({ queryKey: ["applications"] });
    },
  });
}

export function useApplications(params?: Record<string, string | number>) {
  return useQuery({
    queryKey: ["applications", params],
    queryFn: () => applicationsApi.list(params),
  });
}

export function useUpdateApplication() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Application> }) =>
      applicationsApi.update(id, data),
    onSuccess: (updatedApp) => {
      queryClient.setQueriesData(
        { queryKey: ["applications"] },
        (old: PaginatedResponse<Application> | undefined) => {
          if (!old || !old.results) return old;
          return {
            ...old,
            results: old.results.map((app: Application) =>
              app.id === updatedApp.id ? updatedApp : app,
            ),
          };
        },
      );
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });
}

export function useDeleteApplication() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => applicationsApi.delete(id),
    onSuccess: (_data, id) => {
      queryClient.setQueriesData(
        { queryKey: ["applications"] },
        (old: PaginatedResponse<Application> | undefined) => {
          if (!old || !old.results) return old;
          return {
            ...old,
            results: old.results.filter((app: Application) => app.id !== id),
          };
        },
      );
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });
}

export function useUpdateApplicationStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, status }: { id: string; status: ApplicationStatus }) =>
      applicationsApi.update(id, { status }),
    onMutate: async ({ id, status }) => {
      await queryClient.cancelQueries({ queryKey: ["applications"] });
      const previousApplications = queryClient.getQueryData(["applications"]);

      queryClient.setQueriesData(
        { queryKey: ["applications"] },
        (old: PaginatedResponse<Application> | undefined) => {
          if (!old || !old.results) return old;
          return {
            ...old,
            results: old.results.map((app: Application) =>
              app.id === id ? { ...app, status } : app,
            ),
          };
        },
      );

      return { previousApplications };
    },
    onError: (_err, _variables, context) => {
      if (context?.previousApplications) {
        queryClient.setQueriesData(
          { queryKey: ["applications"] },
          context.previousApplications,
        );
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });
}
