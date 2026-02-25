/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState, useMemo } from "react";
import type { ReactNode } from "react";
import type { User, TokenPair } from "../types";
import { api, setTokens, getRefreshToken } from "../api/axios";
import { authApi } from "../api/auth";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (tokens: TokenPair, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const logout = () => {
    setUser(null);
    setTokens(null, null);
    localStorage.removeItem("huntboard_refresh");
  };

  const login = (tokens: TokenPair, user: User) => {
    setTokens(tokens.access, tokens.refresh);
    if (tokens.refresh) {
      localStorage.setItem("huntboard_refresh", tokens.refresh);
    }
    setUser(user);
  };

  useEffect(() => {
    const initializeAuth = async () => {
      // 1. Check if we have a refresh token
      // If the backend uses HttpOnly cookies, we might not have it in localStorage,
      // but we can still try to hit the refresh endpoint
      const storedRefresh = localStorage.getItem("huntboard_refresh");

      try {
        if (storedRefresh) {
          const { access, refresh } = await authApi.refresh(storedRefresh);
          const newRefresh = refresh || storedRefresh;
          setTokens(access, newRefresh);
          if (refresh) {
            localStorage.setItem("huntboard_refresh", refresh);
          }
          const currentUser = await authApi.getMe();
          setUser(currentUser);
        }
      } catch (error) {
        // Token is invalid or expired
        console.error("Failed to initialize auth", error);
        logout();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Setup Axios interceptor to handle 401s and token refresh automatically
  useEffect(() => {
    const responseInterceptor = api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          const refresh =
            getRefreshToken() || localStorage.getItem("huntboard_refresh");

          try {
            // If backend uses cookies, this will still work assuming withCredentials is true
            const response = await api.post<{
              access: string;
              refresh?: string;
            }>("/api/v1/auth/token/refresh/", {
              refresh: refresh || undefined, // Send if we have it manually stored
            });
            const { access, refresh: newRefresh } = response.data;
            const finalRefresh = newRefresh || refresh;
            setTokens(access, finalRefresh);
            if (newRefresh) {
              localStorage.setItem("huntboard_refresh", newRefresh);
            }
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return api(originalRequest);
          } catch (refreshError) {
            logout();
            return Promise.reject(refreshError);
          }
        }
        return Promise.reject(error);
      },
    );

    return () => {
      api.interceptors.response.eject(responseInterceptor);
    };
  }, []);

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout,
    }),
    [user, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
