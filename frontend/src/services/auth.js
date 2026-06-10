import api from './api';

export const authService = {
  register: (userData) =>
    api.post('/auth/register', userData),

  login: (email, password) =>
    api.post('/auth/login', { email, password }),

  logout: () => {
    localStorage.removeItem('token');
  },

  verify: () =>
    api.get('/auth/verify'),

  resetPassword: (token, newPassword) =>
    api.post('/auth/reset-password', { token, newPassword }),

  requestPasswordReset: (email) =>
    api.post('/auth/request-reset', { email }),
};
