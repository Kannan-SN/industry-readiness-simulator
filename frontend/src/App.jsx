import React, { useState, useEffect } from 'react';
import Home from './pages/Home';
import Simulator from './pages/Simulator';
import { apiClient } from './utils/api';
import { Alert, AlertDescription } from './components/ui/alert';
import { AlertCircle, Wifi, WifiOff } from 'lucide-react';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const [error, setError] = useState(null);

  // Check API connection on app start
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await apiClient.healthCheck();
        setConnectionStatus('connected');
      } catch (err) {
        console.log('err: ', err);
        setConnectionStatus('disconnected');
        setError('Unable to connect to the backend API. Please ensure the server is running.');
      }
    };

    checkConnection();
  }, []);

  const handleStartSimulation = () => {
    if (connectionStatus === 'connected') {
      setCurrentPage('simulator');
    }
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setError(null);
  };

  return (
    <div className="min-h-screen">
      {/* Connection Status Banner */}
      {connectionStatus !== 'connected' && (
        <div className={`p-3 text-center text-white ${
          connectionStatus === 'checking' 
            ? 'bg-yellow-600' 
            : 'bg-red-600'
        }`}>
          <div className="flex items-center justify-center gap-2">
            {connectionStatus === 'checking' ? (
              <>
                <Wifi className="w-4 h-4 animate-pulse" />
                Connecting to server...
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4" />
                Server connection failed
              </>
            )}
          </div>
        </div>
      )}

      {/* Error Alert */}
      {error && (
        <div className="container mx-auto px-4 pt-4">
          <Alert className="mb-4 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-700">
              {error}
            </AlertDescription>
          </Alert>
        </div>
      )}

      {/* Main Content */}
      {currentPage === 'home' && (
        <Home onStartSimulation={handleStartSimulation} />
      )}
      
      {currentPage === 'simulator' && (
        <Simulator onBackToHome={handleBackToHome} />
      )}
    </div>
  );
}

export default App;