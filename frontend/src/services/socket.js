import io from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:5000';

let socket = null;

export const socketService = {
  connect: (userId) => {
    if (!socket) {
      socket = io(SOCKET_URL, {
        auth: {
          token: localStorage.getItem('token'),
          userId,
        },
      });
    }
    return socket;
  },

  disconnect: () => {
    if (socket) {
      socket.disconnect();
      socket = null;
    }
  },

  on: (event, callback) => {
    if (socket) {
      socket.on(event, callback);
    }
  },

  emit: (event, data) => {
    if (socket) {
      socket.emit(event, data);
    }
  },

  off: (event) => {
    if (socket) {
      socket.off(event);
    }
  },
};
