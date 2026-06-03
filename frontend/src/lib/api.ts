import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor for JWT
api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Standard Response Wrapper
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  error: string | null;
}

// CRUD Helper Generator
const crud = (endpoint: string) => ({
  list: () => api.get(`${endpoint}/`),
  get: (id: number | string) => api.get(`${endpoint}/${id}/`),
  create: (data: any) => api.post(`${endpoint}/`, data),
  update: (id: number | string, data: any) => api.patch(`${endpoint}/${id}/`, data),
  delete: (id: number | string) => api.delete(`${endpoint}/${id}/`),
});

// Named API Exports
export const authAPI = {
  login: (data: any) => api.post('/auth/login/', data),
  register: (data: any) => api.post('/auth/register/', data),
  profile: () => api.get('/auth/profile/'),
  updateProfile: (data: any) => api.patch('/auth/profile/', data),
};

export const dashboardAPI = {
  stats: () => api.get('/dashboard/stats/'),
};

export const usersAPI = {
  ...crud('/users'),
  approve: (id: number) => api.post(`/users/${id}/approve/`),
  pending: () => api.get('/users/pending/'),
};

export const studentsAPI = crud('/students');
export const teachersAPI = crud('/teachers');
export const coursesAPI = crud('/courses');
export const subjectsAPI = crud('/subjects');
export const assignmentsAPI = crud('/assignments');
export const submissionsAPI = {
  ...crud('/assignment-submissions'),
  grade: (id: number, data: any) => api.patch(`/assignment-submissions/${id}/grade/`, data),
};
export const notesAPI = crud('/notes');
export const videoLecturesAPI = crud('/video-lectures');
export const attendanceAPI = {
  ...crud('/attendance'),
  bulkMark: (data: any) => api.post('/attendance/bulk_mark/', data),
};
export const announcementsAPI = crud('/announcements');
export const eventsAPI = crud('/events');
export const galleryAPI = crud('/gallery');
export const enquiriesAPI = crud('/enquiries');
export const quizzesAPI = crud('/quizzes');
export const paymentsAPI = crud('/payments');
export const resultsAPI = crud('/results');

export default api;
