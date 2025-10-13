import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const api = {
  // Upload and preview CSV file
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.post('/api/upload-csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Filter speakers from CSV file
  filterSpeakersCSV: (eventName, eventTitle = '', file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.post(`/api/filter-speakers-csv?event_name=${encodeURIComponent(eventName)}&event_title=${encodeURIComponent(eventTitle)}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Export speakers from CSV
  exportSpeakersCSV: async (format, eventName, eventTitle = '', file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post(`/api/export-csv/${format}?event_name=${encodeURIComponent(eventName)}&event_title=${encodeURIComponent(eventTitle)}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    link.setAttribute('download', `speaker_report_${timestamp}.${format}`);
    
    document.body.appendChild(link);
    link.click();
    link.remove();
    
    return response;
  },

  // Health check
  healthCheck: () => {
    return apiClient.get('/health');
  },
};

export default api;



