// Helper functions

export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-UG', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const truncateText = (text, length) => {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
};

export const getCrisisKeywords = () => {
  return [
    'suicide',
    'self-harm',
    'kill myself',
    'end my life',
    'hurt myself',
    'cutting',
    'overdose',
  ];
};

export const isValidEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

export const isValidPhoneNumber = (phone) => {
  const regex = /^(\+256|0)[0-9]{9}$/;
  return regex.test(phone);
};
