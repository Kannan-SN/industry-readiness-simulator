SCENARIO_GENERATION_PROMPT = """
You are an expert in creating realistic job scenarios for students. 
Based on the role '{role}' and the provided context, generate a practical scenario that tests real-world skills.

Context: {context}
Role: {role}

Generate a scenario with:
1. Clear task description
2. Realistic requirements
3. Expected deliverables
4. Success criteria

Return as JSON with keys: task, requirements, deliverables, criteria
"""

EVALUATION_PROMPT = """
Evaluate the following student response based on these criteria:
- Clarity (0-25 points)
- Relevance (0-25 points) 
- Correctness (0-25 points)
- Scalability (0-25 points)

Scenario: {scenario}
Student Response: {response}

Provide detailed feedback and scores for each criterion.
Return as JSON with keys: scores, feedback, total_score
"""

GAP_ANALYSIS_PROMPT = """
Based on the evaluation results, identify specific skill gaps:

Evaluation: {evaluation}
Response: {response}

Identify gaps in these categories:
- Technical skills
- Conceptual understanding  
- Process knowledge

Return as JSON with keys: technical_gaps, conceptual_gaps, process_gaps
"""

TRAINING_RECOMMENDATION_PROMPT = """
Based on the identified gaps, recommend specific training resources:

Gaps: {gaps}
Role: {role}

For each gap, suggest:
- Online courses
- Tutorials
- Practice projects
- Documentation

Return as JSON with keys: recommendations (list of resources with title, type, url, description)
"""