from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.settings import settings
from database.weaviate_client import weaviate_client
from services.csv_processor import csv_processor
from database.vector_store import vector_store
from crew.simulator_crew import simulator_crew
from typing import Dict, Any, List
import logging
import json
import tempfile
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Industry-Readiness Combat Simulator",
    description="AI-powered platform for assessing student job readiness",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    try:
        # Test Weaviate Cloud connection
        if weaviate_client.client and weaviate_client.client.is_ready():
            logger.info("Weaviate Cloud connection verified")
        
        # Initialize schema
        weaviate_client.create_schema()
        logger.info("Application startup completed with Weaviate Cloud")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        # Don't raise here to allow API to start even if Weaviate has issues

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        if hasattr(weaviate_client, 'close'):
            weaviate_client.close()
        logger.info("Weaviate Cloud connection closed")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

@app.get("/")
async def root():
    return {"message": "Industry-Readiness Combat Simulator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/upload-scenarios")
async def upload_scenarios(file: UploadFile = File(...)):
    """Upload and process scenario CSV file"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Process CSV and load to vector store
        scenarios = csv_processor.load_scenarios_from_csv(tmp_file_path)
        
        if scenarios:
            vector_store.add_scenarios(scenarios)
            # CRITICAL: Add scenarios to simulator storage
            simulator_crew.add_scenarios_to_storage(scenarios)
            os.unlink(tmp_file_path)  # Clean up temp file
            
            logger.info(f"Successfully uploaded {len(scenarios)} scenarios to both vector store and simulator")
            
            return {
                "message": f"Successfully uploaded {len(scenarios)} scenarios",
                "count": len(scenarios)
            }
        else:
            os.unlink(tmp_file_path)
            raise HTTPException(status_code=400, detail="No valid scenarios found in CSV")
            
    except Exception as e:
        logger.error(f"Scenario upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-training-resources")
async def upload_training_resources(file: UploadFile = File(...)):
    """Upload and process training resources CSV file"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        resources = csv_processor.load_training_resources_from_csv(tmp_file_path)
        
        if resources:
            vector_store.add_training_resources(resources)
            # CRITICAL: Add resources to simulator storage
            simulator_crew.add_training_resources_to_storage(resources)
            os.unlink(tmp_file_path)
            
            logger.info(f"Successfully uploaded {len(resources)} training resources to both vector store and simulator")
            
            return {
                "message": f"Successfully uploaded {len(resources)} training resources",
                "count": len(resources)
            }
        else:
            os.unlink(tmp_file_path)
            raise HTTPException(status_code=400, detail="No valid training resources found in CSV")
            
    except Exception as e:
        logger.error(f"Training resources upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-scenarios")
async def generate_scenarios(student_data: Dict[str, Any]):
    """Generate scenarios for a student"""
    try:
        required_fields = ["role", "skill_level"]
        for field in required_fields:
            if field not in student_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        scenarios = simulator_crew.generate_scenarios_only(student_data)
        
        if not scenarios:
            raise HTTPException(status_code=500, detail="Failed to generate scenarios")
        
        return {
            "scenarios": scenarios,
            "count": len(scenarios)
        }
        
    except Exception as e:
        logger.error(f"Scenario generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-response")
async def submit_response(
    student_data: str = Form(...),
    scenario_id: str = Form(...),
    response_content: str = Form(...),
    files: List[UploadFile] = File(None)
):
    """Submit student response and run complete simulation"""
    try:
        # Parse student data
        student_info = json.loads(student_data)
        
        # Handle file uploads
        file_contents = []
        if files:
            for file in files:
                if file.filename:
                    content = await file.read()
                    file_contents.append({
                        "filename": file.filename,
                        "content": content.decode('utf-8', errors='ignore')
                    })
        
        # Prepare submission data
        submission_data = {
            "student_id": student_info.get("id", "unknown"),
            "scenario_id": scenario_id,
            "content": response_content,
            "files": file_contents
        }
        
        # Run complete simulation
        results = simulator_crew.run_full_simulation(
            student_data=student_info,
            submission_data=submission_data
        )
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return results
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid student data JSON")
    except Exception as e:
        logger.error(f"Response submission failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulation-results/{simulation_id}")
async def get_simulation_results(simulation_id: str):
    """Get simulation results by ID"""
    return {"message": "Results retrieval not implemented yet", "simulation_id": simulation_id}

# DEBUG ENDPOINTS - helpful for testing
@app.get("/debug/scenarios")
async def debug_scenarios():
    """Debug endpoint to see stored scenarios"""
    try:
        return {
            "scenarios": simulator_crew.scenarios_storage, 
            "count": len(simulator_crew.scenarios_storage)
        }
    except Exception as e:
        logger.error(f"Debug scenarios failed: {e}")
        return {"scenarios": [], "count": 0, "error": str(e)}

@app.get("/debug/resources")
async def debug_resources():
    """Debug endpoint to see stored training resources"""
    try:
        return {
            "resources": simulator_crew.training_resources_storage, 
            "count": len(simulator_crew.training_resources_storage)
        }
    except Exception as e:
        logger.error(f"Debug resources failed: {e}")
        return {"resources": [], "count": 0, "error": str(e)}

@app.get("/debug/status")
async def debug_status():
    """Debug endpoint to check system status"""
    try:
        return {
            "weaviate_connected": weaviate_client.client is not None and weaviate_client.client.is_ready() if weaviate_client.client else False,
            "scenarios_loaded": len(simulator_crew.scenarios_storage),
            "resources_loaded": len(simulator_crew.training_resources_storage),
            "api_status": "running"
        }
    except Exception as e:
        return {
            "weaviate_connected": False,
            "scenarios_loaded": 0,
            "resources_loaded": 0,
            "api_status": "error",
            "error": str(e)
        }
        
        
@app.get("/debug/weaviate-data")
async def debug_weaviate_data():
    """Check data in Weaviate Cloud"""
    try:
        if not weaviate_client.client:
            return {"error": "Weaviate client not connected"}
        
        # Check scenarios collection
        scenarios_collection = weaviate_client.client.collections.get("Scenario")
        scenarios_response = scenarios_collection.query.fetch_objects(limit=5)
        scenarios_count = len(scenarios_response.objects)
        
        # Check training resources collection  
        resources_collection = weaviate_client.client.collections.get("TrainingResource")
        resources_response = resources_collection.query.fetch_objects(limit=5)
        resources_count = len(resources_response.objects)
        
        return {
            "weaviate_status": "connected",
            "scenarios_in_weaviate": scenarios_count,
            "resources_in_weaviate": resources_count,
            "sample_scenario": scenarios_response.objects[0].properties if scenarios_response.objects else None,
            "sample_resource": resources_response.objects[0].properties if resources_response.objects else None
        }
    except Exception as e:
        return {"error": f"Weaviate check failed: {e}"}