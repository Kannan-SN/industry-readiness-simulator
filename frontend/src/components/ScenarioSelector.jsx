import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Badge } from './ui/badge';
import { useScenarioGeneration } from '../hooks/useApi';
import { User, Code, Database, BarChart, Globe, Loader2 } from 'lucide-react';

const ScenarioSelector = ({ onScenarioSelect, onStudentDataChange }) => {
  const [studentData, setStudentData] = useState({
    id: '',
    name: '',
    role: '',
    skill_level: '',
    email: ''
  });
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState(null);
  
  const { generateScenarios, loading, error } = useScenarioGeneration();

  const roles = [
    { value: 'frontend', label: 'Frontend Developer', icon: Globe },
    { value: 'backend', label: 'Backend Developer', icon: Database },
    { value: 'data_analyst', label: 'Data Analyst', icon: BarChart },
    { value: 'fullstack', label: 'Full Stack Developer', icon: Code }
  ];

  const skillLevels = [
    { value: 'beginner', label: 'Beginner', description: 'New to the field' },
    { value: 'intermediate', label: 'Intermediate', description: 'Some experience' },
    { value: 'advanced', label: 'Advanced', description: 'Experienced professional' }
  ];

  const handleInputChange = (field, value) => {
    const updatedData = { ...studentData, [field]: value };
    setStudentData(updatedData);
    
    if (onStudentDataChange) {
      onStudentDataChange(updatedData);
    }
  };

  const handleGenerateScenarios = async () => {
    if (!studentData.role || !studentData.skill_level) {
      return;
    }

    try {
      const result = await generateScenarios(studentData);
      setScenarios(result.scenarios || []);
    } catch (err) {
      console.error('Failed to generate scenarios:', err);
    }
  };

  const handleScenarioSelect = (scenario) => {
    setSelectedScenario(scenario);
    if (onScenarioSelect) {
      onScenarioSelect(scenario, studentData);
    }
  };

  const canGenerateScenarios = studentData.role && studentData.skill_level && studentData.name;

  return (
    <div className="space-y-6">
      {/* Student Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <User className="w-5 h-5" />
            Student Information
          </CardTitle>
          <CardDescription>
            Enter your details to get personalized scenarios
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Name</label>
              <Input
                placeholder="Enter your name"
                value={studentData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Email (Optional)</label>
              <Input
                type="email"
                placeholder="your.email@example.com"
                value={studentData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Role</label>
              <Select
                value={studentData.role}
                onValueChange={(value) => handleInputChange('role', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select your role" />
                </SelectTrigger>
                <SelectContent>
                  {roles.map((role) => {
                    const IconComponent = role.icon;
                    return (
                      <SelectItem key={role.value} value={role.value}>
                        <div className="flex items-center gap-2">
                          <IconComponent className="w-4 h-4" />
                          {role.label}
                        </div>
                      </SelectItem>
                    );
                  })}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Skill Level</label>
              <Select
                value={studentData.skill_level}
                onValueChange={(value) => handleInputChange('skill_level', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select skill level" />
                </SelectTrigger>
                <SelectContent>
                  {skillLevels.map((level) => (
                    <SelectItem key={level.value} value={level.value}>
                      <div className="space-y-1">
                        <div className="font-medium">{level.label}</div>
                        <div className="text-xs text-gray-500">{level.description}</div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            onClick={handleGenerateScenarios}
            disabled={!canGenerateScenarios || loading}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Generating Scenarios...
              </>
            ) : (
              'Generate Scenarios'
            )}
          </Button>

          {error && (
            <div className="p-3 bg-red-50 text-red-700 border border-red-200 rounded-lg text-sm">
              Error: {error}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Generated Scenarios */}
      {scenarios.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Available Scenarios</CardTitle>
            <CardDescription>
              Choose a scenario to start your assessment
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {scenarios.map((scenario, index) => (
                <div
                  key={scenario.id || index}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedScenario?.id === scenario.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleScenarioSelect(scenario)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-lg">{scenario.title}</h3>
                      <p className="text-gray-600 mt-1">{scenario.task}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="secondary">{scenario.role}</Badge>
                        <Badge variant="outline">{scenario.difficulty}</Badge>
                      </div>
                      {scenario.requirements && scenario.requirements.length > 0 && (
                        <div className="mt-2">
                          <p className="text-sm font-medium text-gray-700">Requirements:</p>
                          <ul className="text-sm text-gray-600 list-disc list-inside mt-1">
                            {scenario.requirements.slice(0, 2).map((req, i) => (
                              <li key={i}>{req}</li>
                            ))}
                            {scenario.requirements.length > 2 && (
                              <li className="text-gray-500">
                                +{scenario.requirements.length - 2} more...
                              </li>
                            )}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ScenarioSelector;