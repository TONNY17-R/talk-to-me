// Validation functions

export const validateEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

export const validatePassword = (password) => {
  return password.length >= 8;
};

export const validatePhoneNumber = (phone) => {
  const regex = /^(\+256|0)[0-9]{9}$/;
  return regex.test(phone);
};

export const validateName = (name) => {
  return name.length >= 2 && name.length <= 50;
};

export const validateAssessmentAnswers = (answers, questionCount) => {
  return Object.keys(answers).length === questionCount;
};
