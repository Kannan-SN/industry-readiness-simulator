import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { useResponseSubmission } from '../hooks/useApi';
import { Send, Paperclip, FileText, AlertCircle, Clock, Loader2 } from 'lucide-react';

const ResponseSubmission = ({ scenario, studentData, onSubmissionComplete }) => {
  const [responseContent, setResponseContent] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [submissionStatus, setSubmissionStatus] = useState('');
  
  const { submitResponse, loading, error } = useResponseSubmission();

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    setSelectedFiles(files);
  };

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    if (!responseContent.trim()) {
      setSubmissionStatus('Please provide a response before submitting');
      return;
    }

    try {
      setSubmissionStatus('Submitting response...');
      
      const result = await submitResponse(
        studentData,
        scenario.id,
        responseContent,
        selectedFiles
      );

      setSubmissionStatus('Response submitted successfully!');
      
      if (onSubmissionComplete) {
        onSubmissionComplete(result);
      }
    } catch (err) {
      setSubmissionStatus(`Submission failed: ${err.message}`);
    }
  };

  const formatTimeLimit = (timeLimit) => {
    if (!timeLimit) return 'No time limit';
    return timeLimit;
  };

  const getResponsePlaceholder = () => {
    const role = studentData.role;
    
    if (role === 'frontend' || role === 'fullstack') {
      return 'Paste your code here (HTML, CSS, JavaScript, React, etc.)...';
    } else if (role === 'backend') {
      return 'Paste your code here (API endpoints, database schemas, server logic, etc.)...';
    } else if (role === 'data_analyst') {
      return 'Provide your analysis, findings, and conclusions here...';
    }
    
    return 'Enter your solution here...';
  };

  return (
    <div className="space-y-6">
      {/* Scenario Display */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div>
              <CardTitle>{scenario.title}</CardTitle>
              <CardDescription className="mt-2">
                {scenario.task}
              </CardDescription>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <Clock className="w-4 h-4" />
              {formatTimeLimit(scenario.time_limit)}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Badge variant="secondary">{scenario.role}</Badge>
              <Badge variant="outline">{scenario.difficulty}</Badge>
            </div>

            {scenario.requirements && scenario.requirements.length > 0 && (
              <div>
                <h4 className="font-medium text-sm text-gray-700 mb-2">Requirements:</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {scenario.requirements.map((req, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 bg-gray-400 rounded-full mt-2 flex-shrink-0"></span>
                      {req}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {scenario.deliverables && scenario.deliverables.length > 0 && (
              <div>
                <h4 className="font-medium text-sm text-gray-700 mb-2">Expected Deliverables:</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {scenario.deliverables.map((deliverable, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 flex-shrink-0"></span>
                      {deliverable}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Response Submission */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Your Response
          </CardTitle>
          <CardDescription>
            Provide your solution to the scenario above
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Main Response Textarea */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Solution</label>
            <Textarea
              placeholder={getResponsePlaceholder()}
              value={responseContent}
              onChange={(e) => setResponseContent(e.target.value)}
              rows={12}
              className="resize-none font-mono text-sm"
            />
            <div className="text-xs text-gray-500">
              {responseContent.length} characters
            </div>
          </div>

          {/* File Upload */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Additional Files (Optional)</label>
            <Input
              type="file"
              multiple
              onChange={handleFileSelect}
              className="file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            
            {/* Selected Files Display */}
            {selectedFiles.length > 0 && (
              <div className="space-y-2">
                <div className="text-sm font-medium">Selected Files:</div>
                {selectedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-2">
                      <Paperclip className="w-4 h-4 text-gray-500" />
                      <span className="text-sm">{file.name}</span>
                      <Badge variant="secondary" className="text-xs">
                        {(file.size / 1024).toFixed(1)} KB
                      </Badge>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeFile(index)}
                      className="text-red-500 hover:text-red-700"
                    >
                      Remove
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Submit Button */}
          <Button
            onClick={handleSubmit}
            disabled={!responseContent.trim() || loading}
            className="w-full"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Processing Submission...
              </>
            ) : (
              <>
                <Send className="w-4 h-4 mr-2" />
                Submit Response
              </>
            )}
          </Button>

          {/* Status Messages */}
          {submissionStatus && (
            <div className={`flex items-center gap-2 p-3 rounded-lg ${
              submissionStatus.includes('successfully') 
                ? 'bg-green-50 text-green-700 border border-green-200' 
                : submissionStatus.includes('failed')
                ? 'bg-red-50 text-red-700 border border-red-200'
                : 'bg-blue-50 text-blue-700 border border-blue-200'
            }`}>
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">{submissionStatus}</span>
            </div>
          )}

          {error && (
            <div className="flex items-center gap-2 p-3 bg-red-50 text-red-700 border border-red-200 rounded-lg">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">Error: {error}</span>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default ResponseSubmission;