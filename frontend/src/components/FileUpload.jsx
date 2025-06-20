import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { useFileUpload } from '../hooks/useApi';
import { Upload, CheckCircle, AlertCircle, FileText } from 'lucide-react';

const FileUpload = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadType, setUploadType] = useState('scenarios');
  const [uploadStatus, setUploadStatus] = useState('');
  
  const { uploadScenarios, uploadTrainingResources, loading, error } = useFileUpload();

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
      setSelectedFile(file);
      setUploadStatus('');
    } else {
      setUploadStatus('Please select a valid CSV file');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first');
      return;
    }

    try {
      let result;
      if (uploadType === 'scenarios') {
        result = await uploadScenarios(selectedFile);
      } else {
        result = await uploadTrainingResources(selectedFile);
      }

      setUploadStatus(`Success: ${result.message}`);
      setSelectedFile(null);
      
      if (onUploadSuccess) {
        onUploadSuccess(uploadType, result);
      }
    } catch (err) {
      setUploadStatus(`Error: ${err.message}`);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="w-5 h-5" />
          Upload CSV Data
        </CardTitle>
        <CardDescription>
          Upload scenario data or training resources from CSV files
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Upload Type Selection */}
        <div className="flex gap-2">
          <Button
            variant={uploadType === 'scenarios' ? 'default' : 'outline'}
            onClick={() => setUploadType('scenarios')}
            className="flex-1"
          >
            Scenarios
          </Button>
          <Button
            variant={uploadType === 'training' ? 'default' : 'outline'}
            onClick={() => setUploadType('training')}
            className="flex-1"
          >
            Training Resources
          </Button>
        </div>

        {/* File Input */}
        <div className="space-y-2">
          <Input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            disabled={loading}
          />
          {selectedFile && (
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <FileText className="w-4 h-4" />
              {selectedFile.name}
              <Badge variant="secondary">{(selectedFile.size / 1024).toFixed(1)} KB</Badge>
            </div>
          )}
        </div>

        {/* Upload Button */}
        <Button
          onClick={handleUpload}
          disabled={!selectedFile || loading}
          className="w-full"
        >
          {loading ? 'Uploading...' : `Upload ${uploadType === 'scenarios' ? 'Scenarios' : 'Training Resources'}`}
        </Button>

        {/* Status Messages */}
        {uploadStatus && (
          <div className={`flex items-center gap-2 p-3 rounded-lg ${
            uploadStatus.startsWith('Success') 
              ? 'bg-green-50 text-green-700 border border-green-200' 
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}>
            {uploadStatus.startsWith('Success') ? (
              <CheckCircle className="w-4 h-4" />
            ) : (
              <AlertCircle className="w-4 h-4" />
            )}
            <span className="text-sm">{uploadStatus}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-3 bg-red-50 text-red-700 border border-red-200 rounded-lg">
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm">{error}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FileUpload;