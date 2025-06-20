const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // File upload with FormData
  async uploadFile(endpoint, formData) {
    const url = `${this.baseURL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData, // Don't set Content-Type, let browser set it
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(errorData.detail || `Upload failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('File upload failed:', error);
      throw error;
    }
  }

  // API methods
  async uploadScenarios(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.uploadFile('/upload-scenarios', formData);
  }

  async uploadTrainingResources(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.uploadFile('/upload-training-resources', formData);
  }

  async generateScenarios(studentData) {
    return this.request('/generate-scenarios', {
      method: 'POST',
      body: JSON.stringify(studentData),
    });
  }

  async submitResponse(studentData, scenarioId, responseContent, files = []) {
    const formData = new FormData();
    formData.append('student_data', JSON.stringify(studentData));
    formData.append('scenario_id', scenarioId);
    formData.append('response_content', responseContent);
    
    files.forEach(file => {
      formData.append('files', file);
    });

    return this.uploadFile('/submit-response', formData);
  }

  async getSimulationResults(simulationId) {
    return this.request(`/simulation-results/${simulationId}`);
  }

  async healthCheck() {
    return this.request('/health');
  }
}

export const apiClient = new ApiClient();