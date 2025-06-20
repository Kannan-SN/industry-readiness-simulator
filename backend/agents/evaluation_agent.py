from crewai import Agent
from services.llm_service import llm_service
from config.prompts import EVALUATION_PROMPT
from models.response import Evaluation
from typing import Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)

class EvaluationAgent:
    def __init__(self):
        self.agent = Agent(
            role="LLM Evaluator",
            goal="Evaluate student responses using predefined rubrics and provide detailed feedback",
            backstory="Expert evaluator with deep knowledge of industry standards and best practices",
            verbose=True,
            allow_delegation=False
        )
    
    def evaluate_response(self, response_data: Dict[str, Any], scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate student response using LLM with rubrics
        Input: response_data, scenario_data
        Output: Evaluation scores and feedback
        """
        try:
            # Prepare evaluation context
            scenario_context = f"""
            Task: {scenario_data.get('task', '')}
            Requirements: {scenario_data.get('requirements', [])}
            Expected Deliverables: {scenario_data.get('deliverables', [])}
            Success Criteria: {scenario_data.get('criteria', [])}
            """
            
            student_response = response_data.get('content', '')
            response_type = response_data.get('response_type', 'text')
            
            # Create evaluation prompt
            prompt = EVALUATION_PROMPT.format(
                scenario=scenario_context,
                response=student_response
            )
            
            # Add specific criteria based on response type
            if response_type == "code":
                prompt += "\n\nAdditional Code Evaluation Criteria:\n"
                prompt += "- Code structure and organization\n"
                prompt += "- Error handling\n"
                prompt += "- Performance considerations\n"
                prompt += "- Code documentation\n"
            elif response_type == "document":
                prompt += "\n\nAdditional Document Evaluation Criteria:\n"
                prompt += "- Structure and organization\n"
                prompt += "- Supporting evidence\n"
                prompt += "- Professional presentation\n"
            
            # Get evaluation from LLM
            response = llm_service.generate_response(prompt)
            parsed_response = llm_service.parse_json_response(response)
            
            if "error" not in parsed_response:
                # Ensure scores are within valid range
                scores = parsed_response.get("scores", {})
                validated_scores = {}
                
                for criterion, score in scores.items():
                    validated_scores[criterion] = max(0, min(25, int(score))) if isinstance(score, (int, float)) else 0
                
                # Calculate total score
                total_score = sum(validated_scores.values())
                
                evaluation = {
                    "id": str(uuid.uuid4()),
                    "response_id": response_data.get("id", ""),
                    "scores": validated_scores,
                    "feedback": parsed_response.get("feedback", {}),
                    "total_score": total_score,
                    "max_score": 100,
                    "percentage": (total_score / 100) * 100,
                    "grade": self._calculate_grade(total_score),
                    "evaluation_time": response_data.get("submission_time", ""),
                    "response_type": response_type
                }
                
                logger.info(f"Response evaluated with total score: {total_score}/100")
                return evaluation
            else:
                # Return default evaluation if LLM fails
                return self._default_evaluation(response_data)
                
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            return self._default_evaluation(response_data)
    
    def _calculate_grade(self, total_score: int) -> str:
        """Calculate letter grade based on total score"""
        if total_score >= 90:
            return "A"
        elif total_score >= 80:
            return "B"
        elif total_score >= 70:
            return "C"
        elif total_score >= 60:
            return "D"
        else:
            return "F"
    
    def _default_evaluation(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return a default evaluation when LLM evaluation fails"""
        return {
            "id": str(uuid.uuid4()),
            "response_id": response_data.get("id", ""),
            "scores": {"clarity": 15, "relevance": 15, "correctness": 15, "scalability": 15},
            "feedback": {"general": "Unable to evaluate automatically. Manual review required."},
            "total_score": 60,
            "max_score": 100,
            "percentage": 60.0,
            "grade": "D",
            "evaluation_time": response_data.get("submission_time", ""),
            "response_type": response_data.get("response_type", "text"),
            "error": "Automatic evaluation failed"
        }

evaluation_agent = EvaluationAgent()