from crewai import Agent
from services.llm_service import llm_service
from models.scenario import AdaptedChallenge
from typing import Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)

class ChallengePresenterAgent:
    def __init__(self):
        self.agent = Agent(
            role="Challenge Presenter",
            goal="Adapt scenarios to match student skill level and requirements",
            backstory="Expert in customizing challenges based on individual capabilities",
            verbose=True,
            allow_delegation=False
        )
    
    def adapt_challenge(self, scenario: Dict[str, Any], student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt challenge based on student skill level
        Input: scenario, student_profile
        Output: Adapted challenge details
        """
        try:
            skill_level = student_profile.get("skill_level", "beginner")
            role = student_profile.get("role", "")
            
            # Define complexity adjustments
            complexity_map = {
                "beginner": {
                    "level": "Basic",
                    "constraints": ["Step-by-step guidance provided", "Basic requirements only"],
                    "time_limit": "2 hours"
                },
                "intermediate": {
                    "level": "Intermediate", 
                    "constraints": ["Some guidance provided", "Additional requirements"],
                    "time_limit": "1.5 hours"
                },
                "advanced": {
                    "level": "Advanced",
                    "constraints": ["Minimal guidance", "Complex requirements", "Performance optimization needed"],
                    "time_limit": "1 hour"
                }
            }
            
            complexity = complexity_map.get(skill_level, complexity_map["beginner"])
            
            # Create adaptation prompt
            adaptation_prompt = f"""
            Adapt this scenario for a {skill_level} {role} developer:
            
            Original Task: {scenario.get('task', '')}
            Original Requirements: {scenario.get('requirements', [])}
            
            Adjust the complexity to {complexity['level']} level.
            Consider these constraints: {complexity['constraints']}
            Time limit: {complexity['time_limit']}
            
            Provide:
            1. Adapted task description
            2. Specific instructions for {skill_level} level
            3. Expected output format
            4. Success criteria
            
            Return as JSON with keys: adapted_task, instructions, output_format, success_criteria
            """
            
            response = llm_service.generate_response(adaptation_prompt)
            parsed_response = llm_service.parse_json_response(response)
            
            if "error" not in parsed_response:
                adapted_challenge = {
                    "scenario_id": scenario.get("id", ""),
                    "adapted_task": parsed_response.get("adapted_task", scenario.get("task", "")),
                    "complexity_level": skill_level,
                    "constraints": complexity["constraints"],
                    "format_type": "code" if role in ["frontend", "backend", "fullstack"] else "document",
                    "instructions": parsed_response.get("instructions", ""),
                    "output_format": parsed_response.get("output_format", ""),
                    "success_criteria": parsed_response.get("success_criteria", []),
                    "time_limit": complexity["time_limit"]
                }
                
                logger.info(f"Challenge adapted for {skill_level} {role}")
                return adapted_challenge
            else:
                # Return original scenario if adaptation fails
                return {
                    "scenario_id": scenario.get("id", ""),
                    "adapted_task": scenario.get("task", ""),
                    "complexity_level": skill_level,
                    "constraints": complexity["constraints"],
                    "format_type": "code" if role in ["frontend", "backend", "fullstack"] else "document",
                    "instructions": "Complete the given task according to requirements",
                    "time_limit": complexity["time_limit"]
                }
                
        except Exception as e:
            logger.error(f"Challenge adaptation failed: {e}")
            return {}

challenge_presenter_agent = ChallengePresenterAgent()