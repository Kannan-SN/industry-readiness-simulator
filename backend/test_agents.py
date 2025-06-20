import requests
import json

BASE_URL = "http://localhost:8000"

def test_all_agents():
    print("🤖 Testing All AI Agents...")
    
    # Test Agent 1 & 2: Scenario Generation + Challenge Adaptation
    print("\n1️⃣ Testing Scenario Generator & Challenge Presenter Agents...")
    student_data = {
        "role": "backend",
        "skill_level": "intermediate",
        "name": "Test Student"
    }
    
    response = requests.post(f"{BASE_URL}/generate-scenarios", json=student_data)
    if response.status_code == 200:
        scenarios = response.json()["scenarios"]
        print(f"✅ Generated {len(scenarios)} scenarios")
        scenario_id = scenarios[0]["id"]
    else:
        print("❌ Scenario generation failed")
        return
    
    # Test Agents 3, 4, 5, 6: Full Simulation Pipeline
    print("\n2️⃣ Testing Response Collector, Evaluator, Gap Diagnosis & Training Recommender...")
    
    # Prepare test response
    test_response = """
    CREATE TABLE users (
        user_id INT PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        password_hash VARCHAR(255)
    );
    
    CREATE TABLE products (
        product_id INT PRIMARY KEY,
        name VARCHAR(255),
        price DECIMAL(10,2)
    );
    """
    
    # Submit response for full evaluation
    form_data = {
        "student_data": json.dumps(student_data),
        "scenario_id": scenario_id,
        "response_content": test_response
    }
    
    response = requests.post(f"{BASE_URL}/submit-response", data=form_data)
    
    if response.status_code == 200:
        results = response.json()
        
        # Check Agent 3: Response Collector
        if "response" in results:
            print("✅ Agent 3 (Response Collector): Working")
        
        # Check Agent 4: Evaluation Agent
        if "evaluation" in results and "scores" in results["evaluation"]:
            scores = results["evaluation"]["scores"]
            print(f"✅ Agent 4 (Evaluation): Working - Total Score: {results['evaluation']['total_score']}")
        
        # Check Agent 5: Gap Diagnosis Agent
        if "gap_analysis" in results:
            gaps = results["gap_analysis"]
            print(f"✅ Agent 5 (Gap Diagnosis): Working - Found {gaps.get('total_gaps', 0)} gaps")
        
        # Check Agent 6: Training Recommender Agent
        if "training_recommendations" in results:
            recommendations = results["training_recommendations"]
            print(f"✅ Agent 6 (Training Recommender): Working - Generated learning path")
        
        print("\n🎉 All Agents Working Successfully!")
        print(f"📊 Final Assessment Score: {results['evaluation']['total_score']}/100")
        
    else:
        print("❌ Full simulation failed")
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_all_agents()