import api from './api';

export const assessmentService = {
  getAssessments: () =>
    api.get('/assessment'),

  submitAssessment: (assessmentData) =>
    api.post('/assessment', assessmentData),

  getResults: (assessmentId) =>
    api.get(`/assessment/${assessmentId}/results`),

  getHistory: (userId) =>
    api.get(`/assessment/user/${userId}/history`),

  getProgress: (userId) =>
    api.get(`/assessment/user/${userId}/progress`),
};
