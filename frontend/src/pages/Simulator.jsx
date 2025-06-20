import React, { useState } from 'react';
import ScenarioSelector from '../components/ScenarioSelector';
import ResponseSubmission from '../components/ResponseSubmission';
import ResultsDashboard from '../components/ResultsDashboard';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { ArrowLeft, CheckCircle, Clock, FileText } from 'lucide-react';

const Simulator = ({ onBackToHome }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [studentData, setStudentData] = useState(null);
  const [selectedScenario, setSelectedScenario] = useState(null);
  const [simulationResults, setSimulationResults] = useState(null);

  const steps = [
    { number: 1, title: 'Profile Setup', icon: FileText },
    { number: 2, title: 'Complete Scenario', icon: Clock },
    { number: 3, title: 'View Results', icon: CheckCircle }
  ];

  const handleScenarioSelect = (scenario, student) => {
    setSelectedScenario(scenario);
    setStudentData(student);
    setCurrentStep(2);
  };

  const handleSubmissionComplete = (results) => {
    setSimulationResults(results);
    setCurrentStep(3);
  };

  const handleStartNew = () => {
    setCurrentStep(1);
    setStudentData(null);
    setSelectedScenario(null);
    setSimulationResults(null);
  };

  const handleStudentDataChange = (data) => {
    setStudentData(data);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={onBackToHome}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Assessment Simulator</h1>
              <p className="text-gray-600">Complete your industry readiness assessment</p>
            </div>
          </div>
        </div>

        {/* Progress Steps */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Assessment Progress</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              {steps.map((step, index) => {
                const IconComponent = step.icon;
                const isActive = currentStep === step.number;
                const isCompleted = currentStep > step.number;
                
                return (
                  <div key={step.number} className="flex items-center">
                    <div className={`flex items-center gap-2 ${
                      isActive 
                        ? 'text-blue-600' 
                        : isCompleted 
                        ? 'text-green-600' 
                        : 'text-gray-400'
                    }`}>
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 ${
                        isActive 
                          ? 'border-blue-600 bg-blue-50' 
                          : isCompleted 
                          ? 'border-green-600 bg-green-50' 
                          : 'border-gray-300'
                      }`}>
                        {isCompleted ? (
                          <CheckCircle className="w-5 h-5" />
                        ) : (
                          <IconComponent className="w-4 h-4" />
                        )}
                      </div>
                      <span className="font-medium hidden sm:block">{step.title}</span>
                    </div>
                    
                    {index < steps.length - 1 && (
                      <div className={`w-8 h-0.5 mx-4 ${
                        currentStep > step.number ? 'bg-green-600' : 'bg-gray-300'
                      }`} />
                    )}
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Step Content */}
        <div className="max-w-4xl mx-auto">
          {currentStep === 1 && (
            <ScenarioSelector
              onScenarioSelect={handleScenarioSelect}
              onStudentDataChange={handleStudentDataChange}
            />
          )}

          {currentStep === 2 && selectedScenario && studentData && (
            <ResponseSubmission
              scenario={selectedScenario}
              studentData={studentData}
              onSubmissionComplete={handleSubmissionComplete}
            />
          )}

          {currentStep === 3 && simulationResults && (
            <ResultsDashboard
              simulationResults={simulationResults}
              onStartNew={handleStartNew}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Simulator;