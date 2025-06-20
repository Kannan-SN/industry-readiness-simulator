import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { 
  Trophy, 
  Target, 
  TrendingUp, 
  BookOpen, 
  ExternalLink, 
  CheckCircle,
  AlertTriangle,
  Clock,
  Award,
  Star
} from 'lucide-react';

const ResultsDashboard = ({ simulationResults, onStartNew }) => {
  if (!simulationResults || simulationResults.status === 'failed') {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-8">
          <div className="text-center">
            <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Evaluation Failed
            </h3>
            <p className="text-gray-600">
              {simulationResults?.error || 'Unable to process your submission'}
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const { evaluation, gap_analysis, training_recommendations, student, scenario } = simulationResults;

  const getGradeColor = (grade) => {
    const colors = {
      'A': 'bg-green-100 text-green-800 border-green-200',
      'B': 'bg-blue-100 text-blue-800 border-blue-200',
      'C': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'D': 'bg-orange-100 text-orange-800 border-orange-200',
      'F': 'bg-red-100 text-red-800 border-red-200'
    };
    return colors[grade] || colors['F'];
  };

  const getUrgencyColor = (urgency) => {
    if (urgency?.includes('Critical')) return 'destructive';
    if (urgency?.includes('High')) return 'destructive';
    if (urgency?.includes('Medium')) return 'secondary';
    return 'outline';
  };

  const getScoreColor = (score, maxScore = 25) => {
    const percentage = (score / maxScore) * 100;
    if (percentage >= 88) return 'bg-green-600';
    if (percentage >= 72) return 'bg-blue-600';
    if (percentage >= 60) return 'bg-yellow-500';
    if (percentage >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const formatSkills = (skills) => {
    if (!skills) return '';
    return skills.split(' ').slice(0, 3).join(', ');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Assessment Results</h2>
          <p className="text-gray-600">{student.name} • {scenario.title}</p>
        </div>
        <Button onClick={onStartNew} variant="outline">
          Start New Assessment
        </Button>
      </div>

      {/* Overall Score */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="w-5 h-5" />
            Overall Performance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-6">
            <div>
              <div className="text-3xl font-bold text-gray-900">
                {evaluation.total_score}/100
              </div>
              <div className="text-sm text-gray-600">
                {evaluation.percentage?.toFixed(1)}%
              </div>
            </div>
            <div className={`px-4 py-2 rounded-lg border font-bold text-lg ${getGradeColor(evaluation.grade)}`}>
              {evaluation.grade}
            </div>
          </div>
          
          {/* Score Breakdown */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(evaluation.scores || {}).map(([criterion, score]) => (
              <div key={criterion} className="text-center">
                <div className="text-lg font-semibold">{score}/25</div>
                <div className="text-sm text-gray-600 capitalize mb-2">
                  {criterion.replace('_', ' ')}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getScoreColor(score)}`}
                    style={{ width: `${(score / 25) * 100}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {((score / 25) * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Detailed Feedback */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="w-5 h-5" />
            Detailed Feedback
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(evaluation.feedback || {}).map(([criterion, feedback]) => (
              <div key={criterion} className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-medium capitalize text-gray-900">
                  {criterion.replace('_', ' ')}
                </h4>
                <p className="text-gray-600 mt-1">{feedback}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Gap Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Skills Gap Analysis
          </CardTitle>
          <CardDescription>
            Areas identified for improvement
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Improvement Priority:</span>
              <Badge variant={getUrgencyColor(gap_analysis.improvement_urgency)}>
                {gap_analysis.improvement_urgency}
              </Badge>
            </div>

            {/* Priority Areas */}
            {gap_analysis.priority_areas?.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                  <Star className="w-4 h-4 text-yellow-500" />
                  Priority Focus Areas
                </h4>
                <div className="space-y-2">
                  {gap_analysis.priority_areas.map((area, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm text-orange-700 bg-orange-50 p-3 rounded-lg border border-orange-200">
                      <Award className="w-4 h-4 text-orange-500 flex-shrink-0" />
                      <span className="font-medium">{area}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Gap Categories */}
            {gap_analysis.technical_gaps?.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Technical Skills</h4>
                <div className="space-y-1">
                  {gap_analysis.technical_gaps.map((gap, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm text-gray-600">
                      <div className="w-2 h-2 bg-red-400 rounded-full flex-shrink-0"></div>
                      {gap}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {gap_analysis.conceptual_gaps?.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Conceptual Understanding</h4>
                <div className="space-y-1">
                  {gap_analysis.conceptual_gaps.map((gap, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm text-gray-600">
                      <div className="w-2 h-2 bg-yellow-400 rounded-full flex-shrink-0"></div>
                      {gap}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {gap_analysis.process_gaps?.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Process & Methodology</h4>
                <div className="space-y-1">
                  {gap_analysis.process_gaps.map((gap, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm text-gray-600">
                      <div className="w-2 h-2 bg-blue-400 rounded-full flex-shrink-0"></div>
                      {gap}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {gap_analysis.total_gaps === 0 && (
              <div className="flex items-center gap-2 text-green-700 bg-green-50 p-3 rounded-lg">
                <CheckCircle className="w-5 h-5" />
                <span>No significant skill gaps identified. Great job!</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Training Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            Personalized Learning Path
          </CardTitle>
          <CardDescription>
            Recommended resources to improve your skills
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Learning Path Overview */}
            <div className="flex items-center gap-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <Clock className="w-5 h-5 text-blue-600" />
              <div>
                <div className="font-medium text-blue-900">
                  Estimated Duration: {training_recommendations.estimated_duration}
                </div>
                <div className="text-sm text-blue-700">
                  {training_recommendations.urgency}
                </div>
              </div>
            </div>

            {/* Learning Path Phases */}
            {training_recommendations.learning_path?.map((phase, index) => (
              <div key={index} className="border rounded-lg p-4 bg-white shadow-sm">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {phase.phase}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-lg">{phase.title}</h4>
                    <p className="text-sm text-gray-600">{phase.goal}</p>
                    {phase.description && (
                      <p className="text-xs text-gray-500 mt-1">{phase.description}</p>
                    )}
                  </div>
                  <Badge variant="outline" className="ml-auto">
                    {phase.duration}
                  </Badge>
                </div>

                <div className="space-y-3">
                  {phase.resources?.map((resource, resourceIndex) => (
                    <div key={resourceIndex} className="flex items-start justify-between p-3 bg-gray-50 rounded-lg border">
                      <div className="flex-1">
                        <div className="font-medium text-sm text-gray-900">{resource.title}</div>
                        <div className="text-xs text-gray-600 mt-1">{resource.description}</div>
                        {resource.skills && (
                          <div className="text-xs text-blue-600 mt-1">
                            Skills: {formatSkills(resource.skills)}
                          </div>
                        )}
                      </div>
                      <div className="flex items-center gap-2 ml-3">
                        <Badge variant="secondary" className="text-xs">
                          {resource.type}
                        </Badge>
                        {resource.url && resource.url !== '#' && (
                          <Button size="sm" variant="ghost" asChild className="h-8 w-8 p-0">
                            <a href={resource.url} target="_blank" rel="noopener noreferrer" title="Open resource">
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  {(!phase.resources || phase.resources.length === 0) && (
                    <div className="text-sm text-gray-500 italic p-3 bg-gray-50 rounded-lg">
                      No specific resources available for this phase. Please check with your instructor for recommendations.
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* All Recommendations Display */}
            {Object.entries(training_recommendations.recommendations || {}).map(([category, resources]) => (
              resources && resources.length > 0 && (
                <div key={category} className="border rounded-lg p-4 bg-gray-50">
                  <h4 className="font-medium text-gray-900 mb-3 capitalize">
                    {category.replace('_', ' ')} Resources
                  </h4>
                  <div className="space-y-2">
                    {resources.map((resource, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-white rounded border">
                        <div className="flex-1">
                          <div className="font-medium text-sm">{resource.title}</div>
                          <div className="text-xs text-gray-600">{resource.description}</div>
                          {resource.skills && (
                            <div className="text-xs text-blue-600 mt-1">
                              Skills: {formatSkills(resource.skills)}
                            </div>
                          )}
                        </div>
                        <div className="flex items-center gap-2 ml-3">
                          <Badge variant="outline" className="text-xs">
                            {resource.type}
                          </Badge>
                          {resource.url && resource.url !== '#' && (
                            <Button size="sm" variant="ghost" asChild className="h-8 w-8 p-0">
                              <a href={resource.url} target="_blank" rel="noopener noreferrer">
                                <ExternalLink className="w-3 h-3" />
                              </a>
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            ))}

            {/* Priority Actions */}
            {gap_analysis.priority_areas?.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Next Steps:</h4>
                <div className="space-y-2">
                  {gap_analysis.priority_areas.map((action, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm text-gray-700 p-2 bg-yellow-50 rounded border border-yellow-200">
                      <Award className="w-4 h-4 text-yellow-500 flex-shrink-0" />
                      <span>{action}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Summary Statistics */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">
                  {gap_analysis.total_gaps || 0}
                </div>
                <div className="text-xs text-gray-600">Total Gaps Identified</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">
                  {training_recommendations.learning_path?.length || 0}
                </div>
                <div className="text-xs text-gray-600">Learning Phases</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">
                  {Object.values(training_recommendations.recommendations || {}).reduce((total, resources) => total + (resources?.length || 0), 0)}
                </div>
                <div className="text-xs text-gray-600">Recommended Resources</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ResultsDashboard;