from crewai import Agent
from services.llm_service import llm_service
from database.vector_store import vector_store
from config.prompts import TRAINING_RECOMMENDATION_PROMPT
from models.response import TrainingRecommendation
from typing import Dict, Any, List
import logging
import uuid

logger = logging.getLogger(__name__)

class TrainingRecommenderAgent:
    def __init__(self):
        self.agent = Agent(
            role="Training Path Recommender",
            goal="Recommend personalized learning resources based on identified gaps",
            backstory="Expert in educational technology and personalized learning paths",
            verbose=True,
            allow_delegation=False
        )
    
    def recommend_training(self, gap_analysis_data: Dict[str, Any], student_role: str) -> Dict[str, Any]:
        """
        Recommend training resources using RAG from vector store
        Input: gap_analysis_data, student_role
        Output: Personalized training recommendations
        """
        try:
            # Extract gaps for search
            all_gaps = []
            all_gaps.extend(gap_analysis_data.get("technical_gaps", []))
            all_gaps.extend(gap_analysis_data.get("conceptual_gaps", []))
            all_gaps.extend(gap_analysis_data.get("process_gaps", []))
            
            if not all_gaps:
                return self._default_recommendations(student_role)
            
            # Search for relevant training resources in vector store
            search_terms = [student_role] + all_gaps[:3]  # Use top 3 gaps for search
            training_resources = vector_store.search_training_resources(
                skills=search_terms,
                limit=8
            )
            
            # If no resources found in vector store, use LLM to generate recommendations
            if not training_resources:
                training_resources = self._generate_recommendations_with_llm(gap_analysis_data, student_role)
            
            # Categorize recommendations by gap type
            categorized_recommendations = self._categorize_recommendations(
                training_resources, 
                gap_analysis_data
            )
            
            # Create training path with progression
            training_path = self._create_learning_path(categorized_recommendations, gap_analysis_data)
            
            recommendation = {
                "id": str(uuid.uuid4()),
                "gap_analysis_id": gap_analysis_data.get("id", ""),
                "student_role": student_role,
                "recommendations": categorized_recommendations,
                "learning_path": training_path,
                "estimated_duration": self._estimate_duration(training_resources),
                "priority_order": self._prioritize_recommendations(categorized_recommendations),
                "urgency": gap_analysis_data.get("improvement_urgency", "Medium")
            }
            
            logger.info(f"Training recommendations generated for {len(all_gaps)} gaps")
            return recommendation
            
        except Exception as e:
            logger.error(f"Training recommendation failed: {e}")
            return self._default_recommendations(student_role)
    
    def _generate_recommendations_with_llm(self, gap_analysis_data: Dict[str, Any], student_role: str) -> List[Dict[str, Any]]:
        """Generate recommendations using LLM when vector store is empty"""
        try:
            gaps_summary = {
                "technical": gap_analysis_data.get("technical_gaps", []),
                "conceptual": gap_analysis_data.get("conceptual_gaps", []),
                "process": gap_analysis_data.get("process_gaps", [])
            }
            
            prompt = TRAINING_RECOMMENDATION_PROMPT.format(
                gaps=gaps_summary,
                role=student_role
            )
            
            response = llm_service.generate_response(prompt)
            parsed_response = llm_service.parse_json_response(response)
            
            if "error" not in parsed_response:
                return parsed_response.get("recommendations", [])
            else:
                return self._fallback_recommendations(student_role)
                
        except Exception as e:
            logger.error(f"LLM recommendation generation failed: {e}")
            return self._fallback_recommendations(student_role)
    
    def _categorize_recommendations(self, resources: List[Dict[str, Any]], gap_analysis: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize recommendations by gap type and resource type"""
        categorized = {
            "immediate": [],  # Critical skills
            "foundational": [],  # Core concepts
            "advanced": [],  # Enhancement skills
            "practical": []  # Hands-on practice
        }
        
        # Determine urgency level
        urgency = gap_analysis.get("improvement_urgency", "Medium")
        
        for resource in resources:
            resource_type = resource.get("type", "course").lower()
            title = resource.get("title", "").lower()
            
            # Categorize based on resource type and content
            if urgency.startswith("Critical") or "fundamental" in title:
                categorized["immediate"].append(resource)
            elif resource_type in ["course", "tutorial"] and any(word in title for word in ["basics", "introduction", "fundamentals"]):
                categorized["foundational"].append(resource)
            elif resource_type in ["project", "exercise", "practice"]:
                categorized["practical"].append(resource)
            else:
                categorized["advanced"].append(resource)
        
        return categorized
    
    def _create_learning_path(self, categorized_recs: Dict[str, List], gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a structured learning path with progression"""
        learning_path = []
        
        # Phase 1: Immediate/Critical skills
        if categorized_recs["immediate"]:
            learning_path.append({
                "phase": 1,
                "title": "Critical Skills Development",
                "duration": "1-2 weeks",
                "resources": categorized_recs["immediate"][:2],
                "goal": "Address most urgent skill gaps"
            })
        
        # Phase 2: Foundational knowledge
        if categorized_recs["foundational"]:
            learning_path.append({
                "phase": 2,
                "title": "Foundation Building",
                "duration": "2-3 weeks", 
                "resources": categorized_recs["foundational"][:3],
                "goal": "Strengthen core concepts and understanding"
            })
        
        # Phase 3: Practical application
        if categorized_recs["practical"]:
            learning_path.append({
                "phase": 3,
                "title": "Practical Application",
                "duration": "2-4 weeks",
                "resources": categorized_recs["practical"][:2],
                "goal": "Apply knowledge through hands-on practice"
            })
        
        # Phase 4: Advanced skills
        if categorized_recs["advanced"]:
            learning_path.append({
                "phase": 4,
                "title": "Advanced Development",
                "duration": "3-4 weeks",
                "resources": categorized_recs["advanced"][:2],
                "goal": "Develop advanced skills and expertise"
            })
        
        return learning_path
    
    def _estimate_duration(self, resources: List[Dict[str, Any]]) -> str:
        """Estimate total learning duration"""
        total_hours = 0
        
        for resource in resources:
            resource_type = resource.get("type", "course").lower()
            
            # Estimate hours based on resource type
            type_hours = {
                "course": 20,
                "tutorial": 5,
                "documentation": 3,
                "project": 15,
                "practice": 8,
                "book": 30
            }
            
            total_hours += type_hours.get(resource_type, 10)
        
        if total_hours <= 20:
            return "2-3 weeks"
        elif total_hours <= 40:
            return "4-6 weeks"
        elif total_hours <= 60:
            return "6-8 weeks"
        else:
            return "8-12 weeks"
    
    def _prioritize_recommendations(self, categorized_recs: Dict[str, List]) -> List[str]:
        """Create priority order for recommendations"""
        priority_order = []
        
        if categorized_recs["immediate"]:
            priority_order.append("Start with critical skill gaps immediately")
        
        if categorized_recs["foundational"]:
            priority_order.append("Build strong foundations before advancing")
        
        if categorized_recs["practical"]:
            priority_order.append("Practice with hands-on projects")
        
        if categorized_recs["advanced"]:
            priority_order.append("Develop advanced skills for career growth")
        
        return priority_order
    
    def _default_recommendations(self, student_role: str) -> Dict[str, Any]:
        """Provide default recommendations when analysis fails"""
        default_resources = {
            "frontend": [
                {"title": "React Fundamentals", "type": "course", "url": "#", "description": "Learn React basics"},
                {"title": "JavaScript ES6+", "type": "tutorial", "url": "#", "description": "Modern JavaScript features"},
                {"title": "CSS Grid & Flexbox", "type": "practice", "url": "#", "description": "Layout techniques"}
            ],
            "backend": [
                {"title": "REST API Design", "type": "course", "url": "#", "description": "API development principles"},
                {"title": "Database Design", "type": "tutorial", "url": "#", "description": "Database fundamentals"},
                {"title": "Node.js Projects", "type": "project", "url": "#", "description": "Backend development practice"}
            ],
            "data_analyst": [
                {"title": "Python for Data Analysis", "type": "course", "url": "#", "description": "Data analysis with Python"},
                {"title": "SQL Fundamentals", "type": "tutorial", "url": "#", "description": "Database querying"},
                {"title": "Data Visualization", "type": "practice", "url": "#", "description": "Creating meaningful charts"}
            ]
        }
        
        resources = default_resources.get(student_role, default_resources["frontend"])
        
        return {
            "id": str(uuid.uuid4()),
            "gap_analysis_id": "",
            "student_role": student_role,
            "recommendations": {"foundational": resources},
            "learning_path": [
                {
                    "phase": 1,
                    "title": "Foundation Building",
                    "duration": "4-6 weeks",
                    "resources": resources,
                    "goal": "Build core competencies"
                }
            ],
            "estimated_duration": "4-6 weeks",
            "priority_order": ["Start with foundational skills"],
            "urgency": "Medium",
            "note": "Default recommendations - detailed analysis unavailable"
        }
    
    def _fallback_recommendations(self, student_role: str) -> List[Dict[str, Any]]:
        """Fallback recommendations when all else fails"""
        return [
            {"title": f"{student_role.title()} Fundamentals", "type": "course", "url": "#", "description": f"Core {student_role} skills"},
            {"title": "Problem Solving", "type": "tutorial", "url": "#", "description": "Analytical thinking"},
            {"title": "Practice Projects", "type": "project", "url": "#", "description": "Hands-on experience"}
        ]

training_recommender_agent = TrainingRecommenderAgent()