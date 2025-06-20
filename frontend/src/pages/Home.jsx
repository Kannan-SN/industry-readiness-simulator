import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import FileUpload from '../components/FileUpload';
import { 
  Brain, 
  Target, 
  TrendingUp, 
  BookOpen, 
  Upload, 
  Play,
  CheckCircle
} from 'lucide-react';

const Home = ({ onStartSimulation }) => {
  const [uploadedData, setUploadedData] = useState({
    scenarios: false,
    training: false
  });

  const handleUploadSuccess = (type) => {
    setUploadedData(prev => ({
      ...prev,
      [type]: true
    }));
  };

  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Scenarios',
      description: 'Generate realistic job scenarios using advanced AI and industry data'
    },
    {
      icon: Target,
      title: 'Personalized Assessment',
      description: 'Get evaluated based on your role and skill level with detailed feedback'
    },
    {
      icon: TrendingUp,
      title: 'Gap Analysis',
      description: 'Identify specific skill gaps and areas for improvement'
    },
    {
      icon: BookOpen,
      title: 'Learning Recommendations',
      description: 'Receive personalized training paths to enhance your skills'
    }
  ];

  const canStartSimulation = uploadedData.scenarios && uploadedData.training;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Industry-Readiness Combat Simulator
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Test your job readiness with AI-powered scenarios, get detailed feedback, 
            and receive personalized training recommendations to boost your career prospects.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <Card key={index} className="text-center">
                <CardContent className="pt-6">
                  <IconComponent className="w-12 h-12 text-blue-600 mx-auto mb-4" />
                  <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                  <p className="text-gray-600 text-sm">{feature.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Setup Section */}
        <div className="max-w-4xl mx-auto">
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Setup Required
              </CardTitle>
              <CardDescription>
                Upload your CSV data files to get started with personalized scenarios
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <FileUpload onUploadSuccess={handleUploadSuccess} />
                </div>
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Data Requirements</h3>
                  
                  {/* Scenarios CSV Format */}
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      {uploadedData.scenarios ? (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      ) : (
                        <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />
                      )}
                      <span className="font-medium">Scenarios CSV</span>
                    </div>
                    <div className="text-sm text-gray-600 ml-7">
                      Required columns: role, title, task, difficulty, context
                    </div>
                  </div>

                  {/* Training Resources CSV Format */}
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      {uploadedData.training ? (
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      ) : (
                        <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />
                      )}
                      <span className="font-medium">Training Resources CSV</span>
                    </div>
                    <div className="text-sm text-gray-600 ml-7">
                      Required columns: title, type, description, url, skills
                    </div>
                  </div>

                  {/* Sample Data Info */}
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-1">Sample Data Format</h4>
                    <p className="text-sm text-blue-700">
                      Make sure your CSV files have headers and properly formatted data. 
                      Each row should represent one scenario or training resource.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Start Simulation Button */}
          <div className="text-center">
            <Button
              onClick={onStartSimulation}
              disabled={!canStartSimulation}
              size="lg"
              className="px-8 py-3"
            >
              <Play className="w-5 h-5 mr-2" />
              {canStartSimulation ? 'Start Assessment' : 'Upload Data Files First'}
            </Button>
            
            {!canStartSimulation && (
              <p className="text-sm text-gray-500 mt-2">
                Please upload both scenarios and training resources CSV files to begin
              </p>
            )}
          </div>
        </div>

        {/* How It Works Section */}
        <div className="mt-16 max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-semibold mb-2">Select Your Profile</h3>
              <p className="text-gray-600 text-sm">
                Choose your role and skill level to get personalized scenarios
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-semibold mb-2">Complete Scenarios</h3>
              <p className="text-gray-600 text-sm">
                Work on realistic job scenarios adapted to your level
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-semibold mb-2">Get Feedback</h3>
              <p className="text-gray-600 text-sm">
                Receive detailed evaluation and personalized improvement plan
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

