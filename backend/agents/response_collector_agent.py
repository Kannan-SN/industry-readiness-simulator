from crewai import Agent
from models.response import StudentResponse
from typing import Dict, Any, List
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class ResponseCollectorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Response Collector",
            goal="Collect and validate student submissions",
            backstory="Expert in processing various types of student responses and ensuring data integrity",
            verbose=True,
            allow_delegation=False
        )
    
    def collect_response(self, submission_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect and validate student responses
        Input: submission_data (student_id, scenario_id, content, files)
        Output: Structured response data
        """
        try:
            # Validate required fields
            required_fields = ["student_id", "scenario_id", "content"]
            for field in required_fields:
                if field not in submission_data or not submission_data[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            # Determine response type based on content
            content = submission_data["content"]
            response_type = self._determine_response_type(content)
            
            # Validate content based on type
            validation_result = self._validate_content(content, response_type)
            
            if not validation_result["valid"]:
                return {
                    "error": f"Content validation failed: {validation_result['message']}"
                }
            
            # Create structured response
            response = {
                "id": str(uuid.uuid4()),
                "student_id": submission_data["student_id"],
                "scenario_id": submission_data["scenario_id"],
                "response_type": response_type,
                "content": content,
                "files": submission_data.get("files", []),
                "submission_time": datetime.now().isoformat(),
                "content_stats": self._analyze_content(content, response_type),
                "validation": validation_result
            }
            
            logger.info(f"Response collected for student {submission_data['student_id']}")
            return response
            
        except Exception as e:
            logger.error(f"Response collection failed: {e}")
            return {"error": str(e)}
    
    def _determine_response_type(self, content: str) -> str:
        """Determine the type of response based on content analysis"""
        content_lower = content.lower()
        
        # Check for code indicators
        code_indicators = ["function", "class", "def ", "const ", "let ", "var ", "import", "return", "{", "}", "//", "/*"]
        if any(indicator in content_lower for indicator in code_indicators):
            return "code"
        
        # Check for document structure
        doc_indicators = ["introduction", "analysis", "conclusion", "summary", "recommendation"]
        if any(indicator in content_lower for indicator in doc_indicators):
            return "document"
        
        # Check for design elements
        design_indicators = ["schema", "diagram", "architecture", "database", "table", "relationship"]
        if any(indicator in content_lower for indicator in design_indicators):
            return "design"
        
        return "text"
    
    def _validate_content(self, content: str, response_type: str) -> Dict[str, Any]:
        """Validate content based on its type"""
        if not content or len(content.strip()) < 10:
            return {"valid": False, "message": "Content too short or empty"}
        
        if response_type == "code":
            # Basic code validation
            if len(content) < 50:
                return {"valid": False, "message": "Code submission too short"}
            
        elif response_type == "document":
            # Document validation
            if len(content.split()) < 20:
                return {"valid": False, "message": "Document submission too short"}
        
        return {"valid": True, "message": "Content validated successfully"}
    
    def _analyze_content(self, content: str, response_type: str) -> Dict[str, Any]:
        """Analyze content and return statistics"""
        stats = {
            "word_count": len(content.split()),
            "character_count": len(content),
            "line_count": len(content.split('\n')),
            "response_type": response_type
        }
        
        if response_type == "code":
            stats.update({
                "function_count": content.lower().count("function") + content.count("def "),
                "comment_lines": content.count("//") + content.count("#"),
                "has_imports": "import" in content.lower()
            })
        
        return stats

response_collector_agent = ResponseCollectorAgent()