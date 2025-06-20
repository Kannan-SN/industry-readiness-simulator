import pandas as pd
from typing import List, Dict, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CSVProcessor:
    def __init__(self):
        self.data_path = Path("data")
        
    def load_scenarios_from_csv(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(file_path)
            scenarios = []
            
            for _, row in df.iterrows():
                scenario = {
                    "role": row.get("role", "").strip(),
                    "title": row.get("title", "").strip(),
                    "task": row.get("task", "").strip(),
                    "difficulty": row.get("difficulty", "beginner").strip(),
                    "context": row.get("context", "").strip(),
                }
                scenarios.append(scenario)
                
            logger.info(f"Loaded {len(scenarios)} scenarios from CSV")
            return scenarios
        except Exception as e:
            logger.error(f"Failed to load scenarios from CSV: {e}")
            return []
    
    def load_students_from_csv(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(file_path)
            students = []
            
            for _, row in df.iterrows():
                student = {
                    "id": str(row.get("id", "")),
                    "name": row.get("name", "").strip(),
                    "role": row.get("role", "").strip(),
                    "skill_level": row.get("skill_level", "beginner").strip(),
                    "email": row.get("email", "").strip()
                }
                students.append(student)
                
            logger.info(f"Loaded {len(students)} students from CSV")
            return students
        except Exception as e:
            logger.error(f"Failed to load students from CSV: {e}")
            return []
    
    def load_training_resources_from_csv(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(file_path)
            resources = []
            
            for _, row in df.iterrows():
                resource = {
                    "title": row.get("title", "").strip(),
                    "type": row.get("type", "").strip(),
                    "description": row.get("description", "").strip(),
                    "url": row.get("url", "").strip(),
                    "skills": row.get("skills", "").strip()
                }
                resources.append(resource)
                
            logger.info(f"Loaded {len(resources)} training resources from CSV")
            return resources
        except Exception as e:
            logger.error(f"Failed to load training resources from CSV: {e}")
            return []

csv_processor = CSVProcessor()