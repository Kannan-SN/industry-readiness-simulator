from crewai import Task
from typing import Dict, Any

def create_scenario_generation_task(role: str, student_profile: Dict[str, Any]) -> Task:
    return Task(
        description=f"""
        Generate realistic job scenarios for a {role} developer with skill level: {student_profile.get('skill_level', 'beginner')}.
        
        Requirements:
        - Create 3 practical scenarios that test real-world skills
        - Use RAG to retrieve relevant industry scenarios
        - Ensure scenarios are appropriate for the skill level
        - Include clear task descriptions, requirements, and success criteria
        
        Student Profile: {student_profile}
        """,
        expected_output="List of 3 generated scenarios with complete details",
        agent=None  # Will be set in crew
    )

def create_challenge_adaptation_task(scenario: Dict[str, Any], student_profile: Dict[str, Any]) -> Task:
    return Task(
        description=f"""
        Adapt the provided scenario to match the student's skill level and role requirements.
        
        Scenario: {scenario}
        Student: {student_profile}
        
        Requirements:
        - Adjust complexity appropriately
        - Set realistic constraints and time limits
        - Provide clear instructions
        - Define expected output format
        """,
        expected_output="Adapted challenge with specific instructions and requirements",
        agent=None
    )

def create_response_collection_task(submission_data: Dict[str, Any]) -> Task:
    return Task(
        description=f"""
        Collect and validate the student's submission.
        
        Submission: {submission_data}
        
        Requirements:
        - Validate all required fields
        - Determine response type (code, document, design)
        - Check content integrity
        - Generate content statistics
        """,
        expected_output="Structured and validated response data",
        agent=None
    )

def create_evaluation_task(response_data: Dict[str, Any], scenario_data: Dict[str, Any]) -> Task:
    return Task(
        description=f"""
        Evaluate the student response using comprehensive rubrics.
        
        Response: {response_data}
        Scenario: {scenario_data}
        
        Evaluation Criteria:
        - Clarity (0-25 points)
        - Relevance (0-25 points)
        - Correctness (0-25 points)
        - Scalability (0-25 points)
        
        Provide detailed feedback for each criterion.
        """,
        expected_output="Complete evaluation with scores, feedback, and grade",
        agent=None
    )

def create_gap_diagnosis_task(evaluation_data: Dict[str, Any], response_data: Dict[str, Any]) -> Task:
    return Task(
        description=f"""
        Analyze the evaluation results to identify specific skill gaps.
        
        Evaluation: {evaluation_data}
        Response: {response_data}
        
        Requirements:
        - Categorize gaps as technical, conceptual, or process-related
        - Prioritize gaps by importance and impact
        - Determine improvement urgency
        """,
        expected_output="Comprehensive gap analysis with categorized findings",
        agent=None
    )

def create_training_recommendation_task(gap_analysis: Dict[str, Any], student_role: str) -> Task:
    return Task(
        description=f"""
        Recommend personalized training resources based on identified gaps.
        
        Gap Analysis: {gap_analysis}
        Student Role: {student_role}
        
        Requirements:
        - Use RAG to find relevant training resources
        - Create structured learning path with phases
        - Estimate duration and prioritize recommendations
        - Include various resource types (courses, tutorials, projects)
        """,
        expected_output="Personalized training recommendations with learning path",
        agent=None
    )