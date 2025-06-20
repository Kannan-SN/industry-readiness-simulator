from crewai import Agent, Task
from services.llm_service import llm_service
from database.vector_store import vector_store
from config.prompts import SCENARIO_GENERATION_PROMPT
from models.scenario import Role
from typing import Dict, Any, List
import logging
import uuid

logger = logging.getLogger(__name__)

class ScenarioGeneratorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Scenario Generator",
            goal="Generate realistic industry job scenarios for students",
            backstory="Expert in creating practical job scenarios that test real-world skills",
            verbose=True,
            allow_delegation=False
        )
    
    def generate_scenarios(self, role: str, student_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate scenarios using RAG from Weaviate vector store
        Input: role, student_profile
        Output: List of generated scenarios
        """
        try:
            # Search for relevant scenarios in vector store
            existing_scenarios = vector_store.search_scenarios(
                role=role,
                query=f"practical {role} skills assessment",
                limit=3
            )
            
            scenarios = []
            
            if existing_scenarios:
                # Use existing scenarios as context for generation
                for scenario_data in existing_scenarios:
                    context = f"Similar scenario: {scenario_data.get('task', '')}"
                    
                    prompt = SCENARIO_GENERATION_PROMPT.format(
                        role=role,
                        context=context
                    )
                    
                    response = llm_service.generate_response(prompt)
                    parsed_response = llm_service.parse_json_response(response)
                    
                    if "error" not in parsed_response:
                        scenario = {
                            "id": str(uuid.uuid4()),
                            "role": role,
                            "title": parsed_response.get("task", "Untitled Scenario")[:100],
                            "task": parsed_response.get("task", ""),
                            "requirements": parsed_response.get("requirements", []),
                            "deliverables": parsed_response.get("deliverables", []),
                            "criteria": parsed_response.get("criteria", []),
                            "difficulty": student_profile.get("skill_level", "beginner"),
                            "context": context
                        }
                        scenarios.append(scenario)
            else:
                # Generate default scenarios if no existing ones found
                default_contexts = {
                    "frontend": "Build a responsive web application component",
                    "backend": "Design and implement a REST API",
                    "data_analyst": "Analyze business data and create insights",
                    "fullstack": "Create a full-stack web application"
                }
                
                context = default_contexts.get(role, "Create a technical solution")
                prompt = SCENARIO_GENERATION_PROMPT.format(role=role, context=context)
                
                response = llm_service.generate_response(prompt)
                parsed_response = llm_service.parse_json_response(response)
                
                if "error" not in parsed_response:
                    scenario = {
                        "id": str(uuid.uuid4()),
                        "role": role,
                        "title": parsed_response.get("task", "Default Scenario")[:100],
                        "task": parsed_response.get("task", ""),
                        "requirements": parsed_response.get("requirements", []),
                        "deliverables": parsed_response.get("deliverables", []),
                        "criteria": parsed_response.get("criteria", []),
                        "difficulty": student_profile.get("skill_level", "beginner"),
                        "context": context
                    }
                    scenarios.append(scenario)
            
            logger.info(f"Generated {len(scenarios)} scenarios for role: {role}")
            return scenarios
            
        except Exception as e:
            logger.error(f"Scenario generation failed: {e}")
            return []

scenario_generator_agent = ScenarioGeneratorAgent()