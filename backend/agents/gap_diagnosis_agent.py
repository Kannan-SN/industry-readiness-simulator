from crewai import Agent
from services.llm_service import llm_service
from config.prompts import GAP_ANALYSIS_PROMPT
from models.response import GapAnalysis
from typing import Dict, Any, List
import logging
import uuid

logger = logging.getLogger(__name__)

class GapDiagnosisAgent:
    def __init__(self):
        self.agent = Agent(
            role="Gap Diagnosis Specialist",
            goal="Identify specific skill gaps and areas for improvement",
            backstory="Expert in analyzing performance gaps and identifying learning needs",
            verbose=True,
            allow_delegation=False
        )
    
    def diagnose_gaps(self, evaluation_data: Dict[str, Any], response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify skill gaps based on evaluation results
        Input: evaluation_data, response_data
        Output: Categorized gap analysis
        """
        try:
            # Prepare gap analysis context
            evaluation_summary = f"""
            Total Score: {evaluation_data.get('total_score', 0)}/100
            Scores: {evaluation_data.get('scores', {})}
            Feedback: {evaluation_data.get('feedback', {})}
            Grade: {evaluation_data.get('grade', 'Unknown')}
            """
            
            response_summary = f"""
            Response Type: {response_data.get('response_type', 'unknown')}
            Content Length: {len(response_data.get('content', ''))} characters
            Content Stats: {response_data.get('content_stats', {})}
            """
            
            # Create gap analysis prompt
            prompt = GAP_ANALYSIS_PROMPT.format(
                evaluation=evaluation_summary,
                response=response_summary
            )
            
            # Get gap analysis from LLM
            response = llm_service.generate_response(prompt)
            parsed_response = llm_service.parse_json_response(response)
            
            if "error" not in parsed_response:
                # Process and categorize gaps
                technical_gaps = parsed_response.get("technical_gaps", [])
                conceptual_gaps = parsed_response.get("conceptual_gaps", [])
                process_gaps = parsed_response.get("process_gaps", [])
                
                # Add specific gaps based on low scores
                scores = evaluation_data.get('scores', {})
                additional_gaps = self._identify_score_based_gaps(scores, response_data)
                
                # Merge gaps
                technical_gaps.extend(additional_gaps.get("technical", []))
                conceptual_gaps.extend(additional_gaps.get("conceptual", []))
                process_gaps.extend(additional_gaps.get("process", []))
                
                # Remove duplicates
                technical_gaps = list(set(technical_gaps))
                conceptual_gaps = list(set(conceptual_gaps))
                process_gaps = list(set(process_gaps))
                
                gap_analysis = {
                    "id": str(uuid.uuid4()),
                    "evaluation_id": evaluation_data.get("id", ""),
                    "technical_gaps": technical_gaps,
                    "conceptual_gaps": conceptual_gaps,
                    "process_gaps": process_gaps,
                    "total_gaps": len(technical_gaps) + len(conceptual_gaps) + len(process_gaps),
                    "priority_areas": self._prioritize_gaps(technical_gaps, conceptual_gaps, process_gaps),
                    "improvement_urgency": self._calculate_urgency(evaluation_data.get('total_score', 0))
                }
                
                logger.info(f"Gap analysis completed with {gap_analysis['total_gaps']} identified gaps")
                return gap_analysis
            else:
                # Return basic gap analysis based on scores
                return self._basic_gap_analysis(evaluation_data, response_data)
                
        except Exception as e:
            logger.error(f"Gap diagnosis failed: {e}")
            return self._basic_gap_analysis(evaluation_data, response_data)
    
    def _identify_score_based_gaps(self, scores: Dict[str, int], response_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Identify gaps based on low scores in specific areas"""
        gaps = {"technical": [], "conceptual": [], "process": []}
        
        # Define score thresholds for gap identification
        threshold = 18  # Below 18/25 indicates a gap
        
        if scores.get("clarity", 25) < threshold:
            gaps["process"].append("Communication and documentation skills")
            gaps["process"].append("Code/content organization")
        
        if scores.get("relevance", 25) < threshold:
            gaps["conceptual"].append("Understanding of requirements")
            gaps["conceptual"].append("Problem analysis skills")
        
        if scores.get("correctness", 25) < threshold:
            gaps["technical"].append("Implementation accuracy")
            gaps["technical"].append("Solution validation")
        
        if scores.get("scalability", 25) < threshold:
            gaps["technical"].append("Performance optimization")
            gaps["technical"].append("Scalable design patterns")
        
        # Add response-type specific gaps
        response_type = response_data.get("response_type", "")
        if response_type == "code":
            content_stats = response_data.get("content_stats", {})
            if not content_stats.get("has_imports", False):
                gaps["technical"].append("Module management and imports")
            if content_stats.get("comment_lines", 0) < 2:
                gaps["process"].append("Code documentation practices")
        
        return gaps
    
    def _prioritize_gaps(self, technical: List[str], conceptual: List[str], process: List[str]) -> List[str]:
        """Prioritize gaps based on impact and importance"""
        priority_gaps = []
        
        # High priority: Conceptual gaps (affect fundamental understanding)
        if conceptual:
            priority_gaps.append("Conceptual understanding needs improvement")
        
        # Medium priority: Technical gaps (affect implementation)
        if len(technical) > 2:
            priority_gaps.append("Multiple technical skills need development")
        
        # Lower priority: Process gaps (affect methodology)
        if len(process) > 1:
            priority_gaps.append("Process and methodology improvements needed")
        
        return priority_gaps[:3]  # Return top 3 priorities
    
    def _calculate_urgency(self, total_score: int) -> str:
        """Calculate improvement urgency based on total score"""
        if total_score < 50:
            return "Critical - Immediate attention required"
        elif total_score < 70:
            return "High - Significant improvement needed"
        elif total_score < 85:
            return "Medium - Some areas need work"
        else:
            return "Low - Minor improvements suggested"
    
    def _basic_gap_analysis(self, evaluation_data: Dict[str, Any], response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return basic gap analysis when LLM analysis fails"""
        total_score = evaluation_data.get('total_score', 0)
        
        basic_gaps = {
            "technical": ["Implementation skills need improvement"],
            "conceptual": ["Problem understanding needs work"],
            "process": ["Documentation and presentation skills"]
        }
        
        return {
            "id": str(uuid.uuid4()),
            "evaluation_id": evaluation_data.get("id", ""),
            "technical_gaps": basic_gaps["technical"] if total_score < 70 else [],
            "conceptual_gaps": basic_gaps["conceptual"] if total_score < 60 else [],
            "process_gaps": basic_gaps["process"] if total_score < 80 else [],
            "total_gaps": 3 if total_score < 70 else 1,
            "priority_areas": ["General skill improvement needed"],
            "improvement_urgency": self._calculate_urgency(total_score),
            "error": "Detailed analysis unavailable"
        }

gap_diagnosis_agent = GapDiagnosisAgent()