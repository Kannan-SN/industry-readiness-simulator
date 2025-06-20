#!/usr/bin/env python3
"""
Check if scenarios are uploaded to database
Run this to verify your upload status
"""

import weaviate
import requests
import json

# Your Weaviate configuration
WEAVIATE_URL = "https://6y3tmu8jt6gyusexstfoa.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "SkNCaWVyM3pjU0dNT0x5L19XQXdaNHd2c2l4bVo3UmtMZ2hKdE1ucEJXK2NYL3VMb1NBbDJkcjJaN2JjPV92MjAw"

# Your API endpoint
API_BASE = "http://localhost:8000"

def check_weaviate_scenario_data():
    """Check if scenarios are in Weaviate database"""
    print("🔍 Checking Weaviate database for scenarios...")
    
    try:
        client = weaviate.Client(
            url=WEAVIATE_URL,
            auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
        )
        
        if not client.is_ready():
            print("❌ Weaviate not ready")
            return
        
        # Check Scenario class
        try:
            result = client.query.aggregate("Scenario").with_meta_count().do()
            scenario_count = result['data']['Aggregate']['Scenario'][0]['meta']['count']
            print(f"📊 Scenarios in Weaviate: {scenario_count}")
            
            if scenario_count > 0:
                # Get sample scenario
                sample_result = client.query.get("Scenario").with_additional(['id']).with_limit(1).do()
                if 'data' in sample_result and 'Get' in sample_result['data']:
                    sample = sample_result['data']['Get']['Scenario'][0]
                    print(f"✅ Sample scenario found:")
                    for key, value in sample.items():
                        if not key.startswith('_'):
                            print(f"   {key}: {value}")
            else:
                print("📭 No scenarios found in Weaviate")
                
        except Exception as e:
            print(f"❌ Error checking Scenario class: {e}")
        
        # Check TrainingResource class
        try:
            result = client.query.aggregate("TrainingResource").with_meta_count().do()
            resource_count = result['data']['Aggregate']['TrainingResource'][0]['meta']['count']
            print(f"📊 Training Resources in Weaviate: {resource_count}")
        except Exception as e:
            print(f"❌ Error checking TrainingResource class: {e}")
            
    except Exception as e:
        print(f"❌ Weaviate connection error: {e}")

def check_api_debug_endpoints():
    """Check API debug endpoints to see in-memory storage"""
    print("\n🔍 Checking API debug endpoints...")
    
    try:
        # Check debug scenarios
        response = requests.get(f"{API_BASE}/debug/scenarios")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Scenarios in API memory: {data.get('count', 0)}")
            if data.get('scenarios'):
                print(f"✅ Sample scenario from API:")
                sample = data['scenarios'][0]
                for key, value in sample.items():
                    print(f"   {key}: {str(value)[:100]}...")
        else:
            print(f"❌ API scenarios endpoint failed: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        print("❌ API not running. Start with: python main.py")
    except Exception as e:
        print(f"❌ API check error: {e}")
    
    try:
        # Check debug resources
        response = requests.get(f"{API_BASE}/debug/resources")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Resources in API memory: {data.get('count', 0)}")
        else:
            print(f"❌ API resources endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API resources check error: {e}")

def check_api_status():
    """Check overall API status"""
    print("\n🔍 Checking API status...")
    
    try:
        response = requests.get(f"{API_BASE}/debug/status")
        if response.status_code == 200:
            status = response.json()
            print("📋 System Status:")
            print(f"   Weaviate Connected: {'✅' if status.get('weaviate_connected') else '❌'}")
            print(f"   Scenarios Loaded: {status.get('scenarios_loaded', 0)}")
            print(f"   Resources Loaded: {status.get('resources_loaded', 0)}")
            print(f"   API Status: {status.get('api_status', 'unknown')}")
        else:
            print("❌ Status endpoint failed")
    except Exception as e:
        print(f"❌ Status check error: {e}")

def test_scenario_upload():
    """Test uploading scenarios.csv file"""
    print("\n🔍 Testing scenario upload...")
    
    try:
        # Check if scenarios.csv exists
        import os
        if os.path.exists("scenarios.csv"):
            print("✅ scenarios.csv found")
            
            # Try to upload
            with open("scenarios.csv", "rb") as f:
                files = {"file": ("scenarios.csv", f, "text/csv")}
                response = requests.post(f"{API_BASE}/upload-scenarios", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Upload successful: {result.get('message')}")
                    print(f"📊 Uploaded count: {result.get('count')}")
                else:
                    print(f"❌ Upload failed: {response.status_code}")
                    print(f"Error: {response.text}")
        else:
            print("❌ scenarios.csv not found in current directory")
            
    except Exception as e:
        print(f"❌ Upload test error: {e}")

def main():
    """Run all checks"""
    print("🚀 Checking Upload Status for Industry-Readiness Simulator")
    print("=" * 60)
    
    # 1. Check Weaviate database
    check_weaviate_scenario_data()
    
    # 2. Check API endpoints
    check_api_debug_endpoints()
    
    # 3. Check system status
    check_api_status()
    
    # 4. Test upload (optional)
    print("\n" + "=" * 60)
    print("🔧 RECOMMENDATIONS:")
    
    # Analyze and provide recommendations
    try:
        client = weaviate.Client(
            url=WEAVIATE_URL,
            auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
        )
        
        scenario_count = 0
        try:
            result = client.query.aggregate("Scenario").with_meta_count().do()
            scenario_count = result['data']['Aggregate']['Scenario'][0]['meta']['count']
        except:
            pass
        
        if scenario_count == 0:
            print("❌ No scenarios found in database")
            print("📝 TO FIX:")
            print("   1. Make sure your API is running: python main.py")
            print("   2. Upload scenarios.csv via: curl -X POST -F 'file=@scenarios.csv' http://localhost:8000/upload-scenarios")
            print("   3. Check upload with: curl http://localhost:8000/debug/scenarios")
        else:
            print(f"✅ Found {scenario_count} scenarios in database")
            print("🎉 Your data upload is working correctly!")
            
    except Exception as e:
        print(f"❌ Could not determine status: {e}")

if __name__ == "__main__":
    main()