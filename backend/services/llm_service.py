from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.google_api_key,
            temperature=0.7
        )
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise
    
    def parse_json_response(self, response: str) -> dict:
        try:
            # Clean the response to extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:-3]
            elif response.startswith("```"):
                response = response[3:-3]
            
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            # Return a default structure
            return {"error": "Failed to parse LLM response"}

llm_service = LLMService()