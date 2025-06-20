"""
Industry-Readiness Combat Simulator
Main entry point for the backend application
"""

import uvicorn
import logging
import sys
from pathlib import Path

# Add the current directory to Python path to ensure imports work
sys.path.append(str(Path(__file__).parent))

# Import the FastAPI app from api.main
try:
    from api.main import app
    logging.info("Successfully imported FastAPI app")
except ImportError as e:
    logging.error(f"Failed to import FastAPI app: {e}")
    # Try alternative import path
    try:
        from main_api import app
        logging.info("Successfully imported FastAPI app via alternative path")
    except ImportError:
        logging.error("Could not import FastAPI app from any path")
        raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the application"""
    try:
        logger.info("Starting Industry-Readiness Combat Simulator Backend...")
        logger.info("API Documentation will be available at: http://localhost:8000/docs")
        logger.info("Health check endpoint: http://localhost:8000/health")
        logger.info("Debug scenarios: http://localhost:8000/debug/scenarios")
        logger.info("Debug resources: http://localhost:8000/debug/resources")
        
        # Start the FastAPI application with Uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,  # Enable auto-reload during development
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main()