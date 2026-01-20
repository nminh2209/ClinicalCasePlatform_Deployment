// services/auth.ts

import api from "./api";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USER_KEY = "user";

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post("/auth/login/", { email, password });
    const { tokens, user } = response.data;

    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
    localStorage.setItem(USER_KEY, JSON.stringify(user));

    return { tokens, user };
  },

  async register(userData: any) {
    const response = await api.post("/auth/register/", userData);
    const { tokens, user } = response.data;

    localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
    localStorage.setItem(USER_KEY, JSON.stringify(user));

    return { tokens, user };
  },

  async logout() {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
    if (refreshToken) {
      try {
        await api.post("/auth/logout/", { refresh_token: refreshToken });
      } catch (err) {
        console.warn("Logout request failed:", err);
      }
    }
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },

  getCurrentUser() {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
  },

  getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  isAuthenticated() {
    return !!localStorage.getItem(ACCESS_TOKEN_KEY);
  },
};

