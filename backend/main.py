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

# Configure logging with proper file handling
def setup_logging():
    log_file = Path(__file__).parent / 'app.log'
    
    # Create a custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create file handler with proper context management
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Main function to start the application"""
    try:
        logger.info("Starting Industry-Readiness Combat Simulator Backend...")
        logger.info("API Documentation will be available at: http://localhost:8000/docs")
        logger.info("Health check endpoint: http://localhost:8000/health")
        logger.info("Debug scenarios: http://localhost:8000/debug/scenarios")
        logger.info("Debug resources: http://localhost:8000/debug/resources")
        
        # Start the FastAPI application with Uvicorn using import string
        uvicorn.run(
            "api.main:app",  # Use import string instead of app object
            host="0.0.0.0",
            port=8000,
            reload=True,  # Now reload will work properly
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main()