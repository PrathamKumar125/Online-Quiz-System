import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add error handling interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

const quizzesApi = {
  getQuizScores: (quizId) => api.get(`/api/quizzes/${quizId}/scores/`),
  getUserQuizzes: () => api.get('/api/quizzes/user'),
  getAllQuizzes: () => api.get('/api/quizzes/'),
  createQuiz: (quizData) => api.post('/api/quizzes/', quizData),
  mapQuestions: (quizId, questionMaps) => api.post(`/api/quizzes/${quizId}/questions/`, questionMaps),
  get: (quizId) => api.get(`/api/quizzes/${quizId}`),
  startQuizAttempt: (quizId) => api.post(`/api/quizzes/${quizId}/start/`),
  submitQuizAttempt: (quizId, responses) => api.post(`/api/quizzes/${quizId}/submit/`, responses),
  getResponse: (quizId) => api.get(`/api/quizzes/${quizId}/response/`)
};

api.quizzes = quizzesApi;
export { quizzesApi as quizzes };
export default api;