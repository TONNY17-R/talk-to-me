import api from './api';

export const chatService = {
  sendMessage: (message, userId, sessionId) =>
    api.post('/chat/message', { message, userId, sessionId }),

  getHistory: (sessionId) =>
    api.get(`/chat/history/${sessionId}`),

  startSession: (userId) =>
    api.post('/chat/session', { userId }),

  endSession: (sessionId) =>
    api.post(`/chat/session/${sessionId}/end`),

  getEmotionIndicators: (sessionId) =>
    api.get(`/chat/emotions/${sessionId}`),
};
