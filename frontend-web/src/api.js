import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://chemical-backend-y0ii.onrender.com/api';

// Configure axios defaults
axios.defaults.withCredentials = true;

const api = {
  // Health checks
  healthCheck: () => {
    return axios.get('https://chemical-backend-y0ii.onrender.com/health/');
  },
  
  dbCheck: () => {
    return axios.get('https://chemical-backend-y0ii.onrender.com/db-check/');
  },
  
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
  uploadDataset: (formData) => {
    // Ensure formData is FormData object
    if (!(formData instanceof FormData)) {
      const newFormData = new FormData();
      newFormData.append('file', formData);
      formData = newFormData;
    }
    
    return axios.post(`${API_BASE_URL}/datasets/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 second timeout
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
