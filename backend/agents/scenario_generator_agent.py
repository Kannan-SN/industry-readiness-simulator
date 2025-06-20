from crewai import Agent, Task
from services.llm_service import llm_service
from database.vector_store import vector_store
from config.prompts import SCENARIO_GENERATION_PROMPT
from models.scenario import Role
from typing import Dict, Any, List
import logging
import uuid
import time

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
        Generate exactly 3 scenarios using RAG from CSV data in vector store
        Input: role, student_profile
        Output: List of exactly 3 generated scenarios
        """
        start_time = time.time()
        
        try:
            # Target: exactly 3 scenarios as per document requirements
            target_count = 3
            scenarios = []
            
            # Search for relevant scenarios in vector store (from uploaded CSV)
            existing_scenarios = vector_store.search_scenarios(
                role=role,
                query=f"practical {role} skills assessment",
                limit=10  # Get more to have variety for selection
            )
            
            if existing_scenarios and len(existing_scenarios) >= target_count:
                # Filter scenarios by difficulty and role match
                filtered_scenarios = self._filter_scenarios_by_difficulty(
                    existing_scenarios, 
                    student_profile.get("skill_level", "beginner"),
                    role
                )
                
                # If we have enough filtered scenarios, select best 3
                if len(filtered_scenarios) >= target_count:
                    selected_scenarios = filtered_scenarios[:target_count]
                else:
                    # Use all filtered + fill remaining from unfiltered
                    selected_scenarios = filtered_scenarios
                    remaining_needed = target_count - len(filtered_scenarios)
                    additional = [s for s in existing_scenarios if s not in filtered_scenarios][:remaining_needed]
                    selected_scenarios.extend(additional)
                
                # Convert CSV scenarios to required format
                for i, scenario_data in enumerate(selected_scenarios[:target_count]):
                    scenario = self._convert_csv_to_scenario_format(scenario_data, student_profile, i+1)
                    scenarios.append(scenario)
                    
            else:
                # Generate scenarios using LLM if insufficient CSV data
                logger.warning(f"Insufficient scenarios in CSV for role {role}, generating with LLM")
                scenarios = self._generate_scenarios_with_llm(role, student_profile, target_count)
            
            # Ensure we have exactly 3 scenarios
            while len(scenarios) < target_count:
                additional_scenario = self._generate_fallback_scenario(role, student_profile, len(scenarios) + 1)
                scenarios.append(additional_scenario)
            
            # Trim to exactly 3 if we somehow have more
            scenarios = scenarios[:target_count]
            
            # Check processing time requirement (30 seconds max)
            processing_time = time.time() - start_time
            if processing_time > 30:
                logger.warning(f"Scenario generation took {processing_time:.2f}s, exceeds 30s limit")
            
            # Filter outdated/irrelevant scenarios
            scenarios = self._filter_outdated_scenarios(scenarios)
            
            logger.info(f"Generated exactly {len(scenarios)} scenarios for role: {role} in {processing_time:.2f}s")
            return scenarios
            
        except Exception as e:
            logger.error(f"Scenario generation failed: {e}")
            # Return fallback scenarios even on error
            return self._generate_fallback_scenarios(role, student_profile)
    
    def _filter_scenarios_by_difficulty(self, scenarios: List[Dict], skill_level: str, role: str) -> List[Dict]:
        """Filter scenarios based on difficulty and role match"""
        filtered = []
        
        for scenario in scenarios:
            # Check role match (exact or compatible)
            scenario_role = scenario.get("role", "").lower()
            if scenario_role == role.lower() or self._is_compatible_role(scenario_role, role):
                # Check difficulty match
                scenario_difficulty = scenario.get("difficulty", "").lower()
                if scenario_difficulty == skill_level.lower() or skill_level.lower() == "beginner":
                    filtered.append(scenario)
        
        return filtered
    
    def _is_compatible_role(self, scenario_role: str, target_role: str) -> bool:
        """Check if roles are compatible"""
        compatibility_map = {
            "frontend": ["frontend", "fullstack", "web"],
            "backend": ["backend", "fullstack", "api"],
            "fullstack": ["frontend", "backend", "fullstack", "web"],
            "data_analyst": ["data", "analyst", "analytics"]
        }
        
        compatible_roles = compatibility_map.get(target_role.lower(), [target_role.lower()])
        return any(role in scenario_role for role in compatible_roles)
    
    def _convert_csv_to_scenario_format(self, csv_scenario: Dict, student_profile: Dict, scenario_num: int) -> Dict[str, Any]:
        """Convert CSV scenario data to required format"""
        return {
            "id": str(uuid.uuid4()),
            "role": csv_scenario.get("role", ""),
            "title": f"Scenario {scenario_num}: {csv_scenario.get('title', 'Untitled')}",
            "task": csv_scenario.get("task", ""),
            "requirements": self._parse_requirements_from_task(csv_scenario.get("task", "")),
            "deliverables": self._generate_deliverables_from_context(csv_scenario.get("context", "")),
            "criteria": self._generate_criteria_from_task(csv_scenario.get("task", "")),
            "difficulty": csv_scenario.get("difficulty", student_profile.get("skill_level", "beginner")),
            "context": csv_scenario.get("context", ""),
            "source": "csv_data"
        }
    
    def _generate_scenarios_with_llm(self, role: str, student_profile: Dict, count: int) -> List[Dict[str, Any]]:
        """Generate scenarios using LLM when CSV data insufficient"""
        scenarios = []
        
        default_contexts = {
            "frontend": [
                "Build a responsive web application component",
                "Create an interactive dashboard",
                "Develop a mobile-first website"
            ],
            "backend": [
                "Design and implement a REST API",
                "Build a microservices architecture",
                "Create a data processing pipeline"
            ],
            "data_analyst": [
                "Analyze business data and create insights",
                "Build predictive models",
                "Create data visualization dashboard"
            ],
            "fullstack": [
                "Create a full-stack web application",
                "Build an e-commerce platform",
                "Develop a real-time chat application"
            ]
        }
        
        contexts = default_contexts.get(role, default_contexts["frontend"])
        
        for i in range(count):
            context = contexts[i % len(contexts)]
            prompt = SCENARIO_GENERATION_PROMPT.format(role=role, context=context)
            
            response = llm_service.generate_response(prompt)
            parsed_response = llm_service.parse_json_response(response)
            
            if "error" not in parsed_response:
                scenario = {
                    "id": str(uuid.uuid4()),
                    "role": role,
                    "title": f"Scenario {i+1}: {parsed_response.get('task', 'Generated Scenario')[:50]}",
                    "task": parsed_response.get("task", ""),
                    "requirements": parsed_response.get("requirements", []),
                    "deliverables": parsed_response.get("deliverables", []),
                    "criteria": parsed_response.get("criteria", []),
                    "difficulty": student_profile.get("skill_level", "beginner"),
                    "context": context,
                    "source": "llm_generated"
                }
                scenarios.append(scenario)
        
        return scenarios
    
    def _generate_fallback_scenario(self, role: str, student_profile: Dict, scenario_num: int) -> Dict[str, Any]:
        """Generate a single fallback scenario"""
        fallback_tasks = {
            "frontend": f"Create a responsive {['login', 'dashboard', 'profile'][scenario_num % 3]} page",
            "backend": f"Build a {['user management', 'data processing', 'authentication'][scenario_num % 3]} API",
            "data_analyst": f"Analyze {['sales', 'customer', 'inventory'][scenario_num % 3]} data trends",
            "fullstack": f"Develop a {['task management', 'social media', 'e-learning'][scenario_num % 3]} application"
        }
        
        return {
            "id": str(uuid.uuid4()),
            "role": role,
            "title": f"Fallback Scenario {scenario_num}",
            "task": fallback_tasks.get(role, f"Complete a {role} development task"),
            "requirements": [f"Implement core {role} functionality", "Follow best practices"],
            "deliverables": [f"Working {role} solution", "Documentation"],
            "criteria": ["Functionality", "Code quality", "User experience"],
            "difficulty": student_profile.get("skill_level", "beginner"),
            "context": f"Basic {role} development task",
            "source": "fallback"
        }
    
    def _generate_fallback_scenarios(self, role: str, student_profile: Dict) -> List[Dict[str, Any]]:
        """Generate exactly 3 fallback scenarios in case of complete failure"""
        return [
            self._generate_fallback_scenario(role, student_profile, i+1) 
            for i in range(3)
        ]
    
    def _filter_outdated_scenarios(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out outdated or irrelevant scenarios"""
        current_year = 2025
        outdated_keywords = [
            "flash", "internet explorer", "jquery", "php4", "python2", 
            "angularjs", "bootstrap3", "mysql5", "node8"
        ]
        
        filtered_scenarios = []
        for scenario in scenarios:
            task_lower = scenario.get("task", "").lower()
            context_lower = scenario.get("context", "").lower()
            
            # Check for outdated technologies
            is_outdated = any(keyword in task_lower or keyword in context_lower for keyword in outdated_keywords)
            
            if not is_outdated:
                filtered_scenarios.append(scenario)
            else:
                logger.info(f"Filtered outdated scenario: {scenario.get('title', 'Unknown')}")
        
        # If we filtered too many, add some back to maintain count
        if len(filtered_scenarios) < 3:
            filtered_scenarios = scenarios[:3]
        
        return filtered_scenarios
    
    def _parse_requirements_from_task(self, task: str) -> List[str]:
        """Extract requirements from task description"""
        # Basic requirement extraction
        requirements = []
        if "responsive" in task.lower():
            requirements.append("Mobile responsive design")
        if "api" in task.lower():
            requirements.append("RESTful API design")
        if "database" in task.lower():
            requirements.append("Database integration")
        if "secure" in task.lower() or "auth" in task.lower():
            requirements.append("Security implementation")
        
        # Add default requirements if none found
        if not requirements:
            requirements = ["Follow industry best practices", "Clean code structure"]
        
        return requirements
    
    def _generate_deliverables_from_context(self, context: str) -> List[str]:
        """Generate deliverables based on context"""
        deliverables = ["Working solution"]
        
        if "web" in context.lower():
            deliverables.append("Deployed web application")
        if "api" in context.lower():
            deliverables.append("API documentation")
        if "data" in context.lower():
            deliverables.append("Data analysis report")
        
        deliverables.append("Code documentation")
        return deliverables
    
    def _generate_criteria_from_task(self, task: str) -> List[str]:
        """Generate evaluation criteria from task"""
        criteria = ["Functionality", "Code quality"]
        
        if "ui" in task.lower() or "frontend" in task.lower():
            criteria.append("User interface design")
        if "performance" in task.lower():
            criteria.append("Performance optimization")
        if "scale" in task.lower():
            criteria.append("Scalability")
        
        criteria.append("Documentation quality")
        return criteria

scenario_generator_agent = ScenarioGeneratorAgent()