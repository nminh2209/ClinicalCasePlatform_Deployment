import api from "./api";

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post("/auth/login/", { email, password });
    const { tokens, user } = response.data;

    localStorage.setItem("access_token", tokens.access);
    localStorage.setItem("refresh_token", tokens.refresh);
    localStorage.setItem("user", JSON.stringify(user));

    return { tokens, user };
  },

  async register(userData: any) {
    const response = await api.post("/auth/register/", userData);
    const { tokens, user } = response.data;

    localStorage.setItem("access_token", tokens.access);
    localStorage.setItem("refresh_token", tokens.refresh);
    localStorage.setItem("user", JSON.stringify(user));

    return { tokens, user };
  },

  async logout() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (refreshToken) {
      try {
        await api.post("/auth/logout/", { refresh_token: refreshToken });
      } catch (error) {
        console.warn("Logout request failed:", error);
      }
    }
    localStorage.clear();
  },

  getCurrentUser() {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  },

  isAuthenticated() {
    return !!localStorage.getItem("access_token");
  },
};
