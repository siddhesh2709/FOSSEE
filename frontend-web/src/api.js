import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Configure axios defaults
axios.defaults.withCredentials = true;

const api = {
  // Authentication
  login: (username, password) => {
    return axios.post(`${API_BASE_URL}/auth/login/`, { username, password });
  },
  
  logout: () => {
    return axios.post(`${API_BASE_URL}/auth/logout/`);
  },
  
  register: (username, password, email) => {
    return axios.post(`${API_BASE_URL}/auth/register/`, { username, password, email });
  },
  
  getCurrentUser: () => {
    return axios.get(`${API_BASE_URL}/auth/user/`);
  },
  
  // Datasets
  uploadDataset: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_BASE_URL}/datasets/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  getDatasets: () => {
    return axios.get(`${API_BASE_URL}/datasets/`);
  },
  
  getDataset: (id) => {
    return axios.get(`${API_BASE_URL}/datasets/${id}/`);
  },
  
  getDatasetSummary: (id) => {
    return axios.get(`${API_BASE_URL}/datasets/${id}/summary/`);
  },
  
  downloadPDF: (id) => {
    return axios.get(`${API_BASE_URL}/datasets/${id}/pdf/`, {
      responseType: 'blob',
    });
  },
  
  deleteDataset: (id) => {
    return axios.delete(`${API_BASE_URL}/datasets/${id}/`);
  },
};

export default api;
