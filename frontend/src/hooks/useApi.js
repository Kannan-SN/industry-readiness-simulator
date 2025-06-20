import { useState, useCallback } from 'react';
import { apiClient } from '../utils/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (apiCall) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiCall();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, error, execute, setError };
};

// Custom hooks for specific API operations
export const useScenarioGeneration = () => {
  const { loading, error, execute } = useApi();

  const generateScenarios = useCallback(async (studentData) => {
    return execute(() => apiClient.generateScenarios(studentData));
  }, [execute]);

  return { generateScenarios, loading, error };
};

export const useResponseSubmission = () => {
  const { loading, error, execute } = useApi();

  const submitResponse = useCallback(async (studentData, scenarioId, responseContent, files) => {
    return execute(() => apiClient.submitResponse(studentData, scenarioId, responseContent, files));
  }, [execute]);

  return { submitResponse, loading, error };
};

export const useFileUpload = () => {
  const { loading, error, execute } = useApi();

  const uploadScenarios = useCallback(async (file) => {
    return execute(() => apiClient.uploadScenarios(file));
  }, [execute]);

  const uploadTrainingResources = useCallback(async (file) => {
    return execute(() => apiClient.uploadTrainingResources(file));
  }, [execute]);

  return { uploadScenarios, uploadTrainingResources, loading, error };
};