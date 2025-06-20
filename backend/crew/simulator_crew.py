import logging
import uuid

logger = logging.getLogger(__name__)

class SimulatorCrew:
    def __init__(self):
        # Initialize storage as instance variables
        self.scenarios_storage = []
        self.training_resources_storage = []
        logger.info("SimulatorCrew initialized with empty storage")
    
    def add_scenarios_to_storage(self, scenarios):
        """Add scenarios to instance storage"""
        self.scenarios_storage.extend(scenarios)
        logger.info(f"Added {len(scenarios)} scenarios to storage. Total: {len(self.scenarios_storage)}")
        # Debug log first few scenarios
        for i, scenario in enumerate(scenarios[:2]):
            logger.info(f"Scenario {i+1}: {scenario.get('title', 'No title')} - Role: {scenario.get('role', 'No role')}")
    
    def add_training_resources_to_storage(self, resources):
        """Add training resources to instance storage"""
        self.training_resources_storage.extend(resources)
        logger.info(f"Added {len(resources)} training resources to storage. Total: {len(self.training_resources_storage)}")
        # Debug log first few resources
        for i, resource in enumerate(resources[:2]):
            logger.info(f"Resource {i+1}: {resource.get('title', 'No title')} - Type: {resource.get('type', 'No type')}")
    
    def generate_scenarios_only(self, student_data):
        logger.info("Generating scenarios...")
        role = student_data.get("role", "frontend")
        skill_level = student_data.get("skill_level", "beginner")
        
        logger.info(f"Looking for scenarios for role: {role}, skill: {skill_level}")
        logger.info(f"Available scenarios in storage: {len(self.scenarios_storage)}")
        
        # First, try to get scenarios from uploaded CSV data
        uploaded_scenarios = []
        try:
            uploaded_scenarios = [s for s in self.scenarios_storage if s.get("role", "").lower() == role.lower()]
            logger.info(f"Found {len(uploaded_scenarios)} matching scenarios for role: {role}")
        except Exception as e:
            logger.warning(f"Could not retrieve uploaded scenarios: {e}")
        
        scenarios = []
        
        # Use uploaded scenarios if available
        if uploaded_scenarios:
            logger.info("Using uploaded scenarios from CSV")
            for scenario_data in uploaded_scenarios[:2]:  # Take first 2
                scenario = {
                    "id": str(uuid.uuid4()),
                    "title": scenario_data.get("title", f"{role.title()} Challenge"),
                    "task": scenario_data.get("task", f"Complete a {role} development task"),
                    "role": role,
                    "difficulty": skill_level,
                    "context": scenario_data.get("context", ""),
                    "requirements": self._split_field(scenario_data.get("requirements", [])),
                    "deliverables": self._split_field(scenario_data.get("deliverables", [])),
                    "criteria": self._split_field(scenario_data.get("criteria", []))
                }
                scenarios.append(scenario)
        
        # If no uploaded scenarios or need more, generate default ones
        if len(scenarios) < 2:
            logger.info("Using default scenarios (no CSV data found)")
            default_scenarios = self._generate_default_scenarios(role, skill_level)
            scenarios.extend(default_scenarios[:(2 - len(scenarios))])
        
        logger.info(f"Generated {len(scenarios)} scenarios for {role}")
        return scenarios
    
    def _split_field(self, field):
        """Helper to split comma-separated fields"""
        if isinstance(field, str):
            return [item.strip() for item in field.split(",") if item.strip()]
        elif isinstance(field, list):
            return field
        else:
            return []
    
    def _generate_default_scenarios(self, role, skill_level):
        """Generate default scenarios when no CSV data is available"""
        if role == "frontend":
            return [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Responsive Product Page",
                    "task": "Create a responsive e-commerce product page with add to cart functionality",
                    "role": role,
                    "difficulty": skill_level,
                    "requirements": ["React components", "Responsive design", "State management"],
                    "deliverables": ["Working product page", "Mobile-responsive design"],
                    "criteria": ["Code quality", "User experience", "Performance"]
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Interactive Dashboard",
                    "task": "Build a data visualization dashboard with charts and filters",
                    "role": role,
                    "difficulty": skill_level,
                    "requirements": ["Chart library integration", "Interactive filters", "Data handling"],
                    "deliverables": ["Functional dashboard", "Interactive components"],
                    "criteria": ["Visualization quality", "Interactivity", "Code structure"]
                }
            ]
        elif role == "backend":
            return [
                {
                    "id": str(uuid.uuid4()),
                    "title": "REST API Development",
                    "task": "Design and implement a RESTful API for a blog platform",
                    "role": role,
                    "difficulty": skill_level,
                    "requirements": ["CRUD operations", "Authentication", "Database integration"],
                    "deliverables": ["API endpoints", "Documentation", "Error handling"],
                    "criteria": ["API design", "Security", "Performance"]
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "Database Design",
                    "task": "Create a database schema for an e-commerce platform",
                    "role": role,
                    "difficulty": skill_level,
                    "requirements": ["Entity relationships", "Normalization", "Indexing"],
                    "deliverables": ["Schema design", "Sample queries", "Documentation"],
                    "criteria": ["Schema quality", "Optimization", "Scalability"]
                }
            ]
        elif role == "data_analyst":
            return [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Sales Data Analysis",
                    "task": "Analyze quarterly sales data and identify key trends",
                    "role": role,
                    "difficulty": skill_level,
                    "requirements": ["Data cleaning", "Statistical analysis", "Visualization"],
                    "deliverables": ["Analysis report", "Charts and graphs", "Recommendations"],
                    "criteria": ["Analytical accuracy", "Insight quality", "Presentation"]
                }
            ]
        else:  # fullstack
            return [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Full-Stack Application",
                    "task": "Build a complete task management application",
                    "role": role,
                    "difficulty": skill_level,
                    "requirements": ["Frontend UI", "Backend API", "Database"],
                    "deliverables": ["Complete application", "User authentication", "CRUD functionality"],
                    "criteria": ["Architecture", "User experience", "Code quality"]
                }
            ]
    
    def run_full_simulation(self, student_data, submission_data):
        logger.info("Running full simulation...")
        logger.info(f"Available training resources: {len(self.training_resources_storage)}")
        
        # Simple evaluation logic (enhanced from previous version)
        content = submission_data.get("content", "")
        content_length = len(content)
        word_count = len(content.split())
        
        # Analyze response content for better scoring
        has_code = any(keyword in content.lower() for keyword in 
                      ['create table', 'select', 'insert', 'update', 'delete', 'function', 'class', 'def ', 'const ', 'let ', 'var '])
        has_structure = any(keyword in content.lower() for keyword in 
                           ['primary key', 'foreign key', 'index', 'constraint', 'return', '{', '}', 'if', 'for'])
        has_comments = '--' in content or '//' in content or '#' in content or '/*' in content
        has_best_practices = any(keyword in content.lower() for keyword in 
                               ['not null', 'unique', 'auto_increment', 'timestamp', 'varchar'])
        
        # Enhanced scoring based on content analysis
        clarity_score = min(25, max(5, content_length // 20))
        if has_comments:
            clarity_score = min(25, clarity_score + 5)
        if content_length > 500:
            clarity_score = min(25, clarity_score + 3)
        
        relevance_score = 15
        if has_code:
            relevance_score += 5
        if has_structure:
            relevance_score += 3
        if word_count > 50:
            relevance_score += 2
        relevance_score = min(25, relevance_score)
        
        correctness_score = 12
        if has_structure:
            correctness_score += 8
        if has_best_practices:
            correctness_score += 5
        correctness_score = min(25, correctness_score)
        
        scalability_score = min(25, max(10, content_length // 30))
        if 'index' in content.lower():
            scalability_score = min(25, scalability_score + 5)
        if any(keyword in content.lower() for keyword in ['performance', 'optimization', 'efficient']):
            scalability_score = min(25, scalability_score + 3)
        
        total_score = clarity_score + relevance_score + correctness_score + scalability_score
        
        # Determine grade
        if total_score >= 90:
            grade = "A"
        elif total_score >= 80:
            grade = "B"
        elif total_score >= 70:
            grade = "C"
        elif total_score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        # Enhanced gap analysis
        technical_gaps = []
        conceptual_gaps = []
        process_gaps = []
        
        if correctness_score < 20:
            technical_gaps.extend(["Implementation accuracy", "Code structure", "Syntax knowledge"])
        if scalability_score < 20:
            technical_gaps.extend(["Performance optimization", "Scalable design patterns"])
        if clarity_score < 20:
            process_gaps.extend(["Code documentation", "Code organization", "Communication skills"])
        if relevance_score < 20:
            conceptual_gaps.extend(["Understanding of requirements", "Problem analysis skills"])
        
        # Additional specific gaps based on content
        if 'foreign key' not in content.lower() and 'join' not in content.lower():
            technical_gaps.append("Database relationships and constraints")
        if 'index' not in content.lower():
            technical_gaps.append("Database performance optimization")
        if not has_comments:
            process_gaps.append("Code documentation practices")
        
        # Remove duplicates
        technical_gaps = list(set(technical_gaps))
        conceptual_gaps = list(set(conceptual_gaps))
        process_gaps = list(set(process_gaps))
        
        # Improvement urgency
        if total_score < 50:
            urgency = "Critical - Immediate attention required"
        elif total_score < 70:
            urgency = "High - Significant improvement needed"
        elif total_score < 85:
            urgency = "Medium - Some areas need work"
        else:
            urgency = "Low - Minor improvements suggested"
        
        # CRITICAL: Enhanced training recommendations using uploaded CSV data
        role = student_data.get("role", "")
        recommendations = self._get_detailed_training_recommendations(role, technical_gaps, conceptual_gaps, process_gaps)
        
        # Create detailed learning path
        learning_path = self._create_detailed_learning_path(recommendations, urgency)
        
        # Find the original scenario
        original_scenario = None
        scenario_id = submission_data.get("scenario_id", "")
        for scenario in self.scenarios_storage:
            if scenario.get("id") == scenario_id:
                original_scenario = scenario
                break
        
        if not original_scenario:
            original_scenario = {
                "id": scenario_id,
                "title": "Assessment Scenario",
                "task": "Complete the assigned task",
                "role": role,
                "difficulty": student_data.get("skill_level", "beginner")
            }
        
        # Compile comprehensive results
        results = {
            "simulation_id": str(uuid.uuid4()),
            "student": student_data,
            "scenario": original_scenario,
            "adapted_challenge": {
                "scenario_id": scenario_id,
                "adapted_task": original_scenario.get("task", ""),
                "complexity_level": student_data.get("skill_level", "beginner"),
                "instructions": "Complete the task according to the requirements"
            },
            "response": {
                "id": str(uuid.uuid4()),
                "content": content,
                "word_count": word_count,
                "has_code": has_code,
                "content_stats": {
                    "length": content_length,
                    "words": word_count,
                    "has_structure": has_structure,
                    "has_comments": has_comments,
                    "has_best_practices": has_best_practices
                }
            },
            "evaluation": {
                "id": str(uuid.uuid4()),
                "scores": {
                    "clarity": clarity_score,
                    "relevance": relevance_score,
                    "correctness": correctness_score,
                    "scalability": scalability_score
                },
                "total_score": total_score,
                "grade": grade,
                "percentage": (total_score / 100) * 100,
                "feedback": {
                    "clarity": f"Code clarity: {'Excellent' if clarity_score >= 22 else 'Good' if clarity_score >= 18 else 'Needs improvement'} ({clarity_score}/25)",
                    "relevance": f"Task relevance: {'Excellent' if relevance_score >= 22 else 'Good' if relevance_score >= 18 else 'Could be better'} ({relevance_score}/25)",
                    "correctness": f"Implementation: {'Excellent' if correctness_score >= 22 else 'Good' if correctness_score >= 18 else 'Needs work'} ({correctness_score}/25)",
                    "scalability": f"Scalability: {'Excellent' if scalability_score >= 22 else 'Good' if scalability_score >= 18 else 'Consider improvements'} ({scalability_score}/25)",
                    "general": f"Overall performance shows {'excellent' if total_score >= 85 else 'good' if total_score >= 70 else 'basic'} understanding of the requirements."
                }
            },
            "gap_analysis": {
                "id": str(uuid.uuid4()),
                "technical_gaps": technical_gaps,
                "conceptual_gaps": conceptual_gaps,
                "process_gaps": process_gaps,
                "total_gaps": len(technical_gaps) + len(conceptual_gaps) + len(process_gaps),
                "improvement_urgency": urgency,
                "priority_areas": self._get_priority_areas(technical_gaps, conceptual_gaps, process_gaps)
            },
            "training_recommendations": {
                "id": str(uuid.uuid4()),
                "student_role": role,
                "recommendations": recommendations,
                "learning_path": learning_path,
                "estimated_duration": self._estimate_total_duration(learning_path),
                "urgency": urgency
            },
            "status": "completed",
            "timestamp": str(uuid.uuid4())
        }
        
        logger.info(f"Completed simulation for student {student_data.get('name', 'Unknown')} with score {total_score}")
        return results
    
    def _get_detailed_training_recommendations(self, role, technical_gaps, conceptual_gaps, process_gaps):
        """Get detailed training recommendations from uploaded CSV data"""
        logger.info(f"Getting training recommendations for role: {role}")
        logger.info(f"Technical gaps: {technical_gaps}")
        logger.info(f"Available resources: {len(self.training_resources_storage)}")
        
        recommendations = {
            "immediate": [],
            "foundational": [],
            "practical": [],
            "advanced": []
        }
        
        # Search uploaded training resources
        role_resources = []
        gap_keywords = technical_gaps + conceptual_gaps + process_gaps
        
        logger.info(f"Searching for resources matching role '{role}' or gaps: {gap_keywords}")
        
        for resource in self.training_resources_storage:
            resource_skills = str(resource.get("skills", "")).lower()
            resource_title = str(resource.get("title", "")).lower()
            resource_description = str(resource.get("description", "")).lower()
            
            # Check if resource matches role or gaps
            role_match = role.lower() in resource_skills or role.lower() in resource_title
            gap_match = any(gap.lower() in resource_skills or gap.lower() in resource_title or gap.lower() in resource_description 
                           for gap in gap_keywords)
            
            if role_match or gap_match:
                role_resources.append(resource)
                logger.info(f"Found matching resource: {resource.get('title', 'Unknown')}")
        
        logger.info(f"Found {len(role_resources)} matching resources")
        
        # Categorize resources
        for resource in role_resources:
            resource_type = str(resource.get("type", "course")).lower()
            title = str(resource.get("title", "")).lower()
            
            if any(urgent_word in title for urgent_word in ["fundamental", "basic", "introduction", "beginner"]):
                recommendations["foundational"].append(resource)
            elif resource_type in ["project", "exercise", "practice"]:
                recommendations["practical"].append(resource)
            elif any(advanced_word in title for advanced_word in ["advanced", "expert", "master", "optimization"]):
                recommendations["advanced"].append(resource)
            else:
                recommendations["immediate"].append(resource)
        
        # If no uploaded resources found, use defaults
        if not any(recommendations.values()):
            logger.warning("No matching resources found, using default recommendations")
            recommendations = self._get_default_recommendations(role)
        else:
            logger.info(f"Using {sum(len(resources) for resources in recommendations.values())} resources from CSV")
        
        return recommendations
    
    def _get_default_recommendations(self, role):
        """Fallback recommendations when no CSV data is available"""
        if role == "frontend":
            return {
                "foundational": [
                    {"title": "React Fundamentals", "type": "course", "description": "Learn React basics", "url": "#", "skills": "React JavaScript"},
                    {"title": "JavaScript ES6+", "type": "tutorial", "description": "Modern JavaScript", "url": "#", "skills": "JavaScript ES6"},
                    {"title": "CSS Grid & Flexbox", "type": "tutorial", "description": "Layout techniques", "url": "#", "skills": "CSS layout"}
                ],
                "practical": [
                    {"title": "React Portfolio Project", "type": "project", "description": "Build portfolio", "url": "#", "skills": "React project"}
                ]
            }
        elif role == "backend":
            return {
                "foundational": [
                    {"title": "SQL Database Design", "type": "course", "description": "Database fundamentals", "url": "#", "skills": "SQL database"},
                    {"title": "Node.js Development", "type": "course", "description": "Backend development", "url": "#", "skills": "Node.js backend"},
                    {"title": "API Development", "type": "tutorial", "description": "REST API design", "url": "#", "skills": "API REST"}
                ]
            }
        elif role == "data_analyst":
            return {
                "foundational": [
                    {"title": "Python for Data Analysis", "type": "course", "description": "Data analysis with Python", "url": "#", "skills": "Python data analysis"},
                    {"title": "SQL Fundamentals", "type": "tutorial", "description": "Database querying", "url": "#", "skills": "SQL database"},
                    {"title": "Data Visualization", "type": "course", "description": "Creating charts", "url": "#", "skills": "visualization charts"}
                ]
            }
        else:
            return {
                "foundational": [
                    {"title": "Full Stack Development", "type": "course", "description": "Complete web development", "url": "#", "skills": "fullstack development"},
                    {"title": "Software Architecture", "type": "tutorial", "description": "System design", "url": "#", "skills": "architecture design"}
                ]
            }
    
    def _create_detailed_learning_path(self, recommendations, urgency):
        """Create a structured learning path with detailed phases"""
        learning_path = []
        
        # Phase 1: Immediate/Critical skills
        if recommendations.get("immediate") or recommendations.get("foundational"):
            phase1_resources = (recommendations.get("immediate", []) + recommendations.get("foundational", []))[:3]
            if phase1_resources:
                learning_path.append({
                    "phase": 1,
                    "title": "Foundation Building",
                    "duration": "2-3 weeks",
                    "resources": phase1_resources,
                    "goal": "Strengthen core concepts and skills",
                    "description": "Focus on fundamental knowledge and essential skills"
                })
        
        # Phase 2: Practical application
        if recommendations.get("practical"):
            learning_path.append({
                "phase": 2,
                "title": "Practical Application",
                "duration": "3-4 weeks",
                "resources": recommendations["practical"][:2],
                "goal": "Apply knowledge through hands-on practice",
                "description": "Build real projects to reinforce learning"
            })
        
        # Phase 3: Advanced skills
        if recommendations.get("advanced"):
            learning_path.append({
                "phase": 3,
                "title": "Advanced Development",
                "duration": "2-3 weeks",
                "resources": recommendations["advanced"][:2],
                "goal": "Develop advanced skills and expertise",
                "description": "Master advanced concepts and techniques"
            })
        
        return learning_path
    
    def _estimate_total_duration(self, learning_path):
        """Estimate total learning duration"""
        if not learning_path:
            return "4-6 weeks"
        
        total_weeks = 0
        for phase in learning_path:
            duration = phase.get("duration", "2-3 weeks")
            # Extract max weeks from duration string
            if "2-3" in duration:
                total_weeks += 3
            elif "3-4" in duration:
                total_weeks += 4
            else:
                total_weeks += 3
        
        if total_weeks <= 6:
            return "4-6 weeks"
        elif total_weeks <= 10:
            return "6-10 weeks"
        else:
            return "10-12 weeks"
    
    def _get_priority_areas(self, technical_gaps, conceptual_gaps, process_gaps):
        """Determine priority improvement areas"""
        priorities = []
        
        if conceptual_gaps:
            priorities.append("Conceptual understanding needs strengthening")
        if len(technical_gaps) > 2:
            priorities.append("Multiple technical skills require development")
        if process_gaps:
            priorities.append("Process and methodology improvements needed")
        
        return priorities[:3]  # Return top 3 priorities

# Create the instance
simulator_crew = SimulatorCrew()