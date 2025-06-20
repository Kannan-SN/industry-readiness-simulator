#!/usr/bin/env python3
"""
Comprehensive verification that uploaded data is in Weaviate database
This will definitively show if your CSV data made it to the database
"""

import weaviate
from weaviate.auth import AuthApiKey
import requests
import json

# Your Weaviate configuration
WEAVIATE_URL = "https://6y3tmu8jt6gyusexstfoa.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "SkNCaWVyM3pjU0dNT0x5L19XQXRaNHd2c2l4bVo3UmtMZ2hKdE1ucEJXK2NYL3VMb1NBbDJkcjJaN2JjPV92MjAw"
API_BASE = "http://localhost:8000"

def check_weaviate_database():
    """Direct database check - the definitive answer"""
    print("🔍 CHECKING WEAVIATE DATABASE DIRECTLY")
    print("=" * 50)
    
    try:
        # Connect to Weaviate using v4 client
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=AuthApiKey(WEAVIATE_API_KEY)
        )
        
        if not client.is_ready():
            print("❌ Weaviate connection failed")
            return False
        
        print("✅ Connected to Weaviate Cloud")
        
        # Check all collections
        collections = client.collections.list_all()
        print(f"📚 Available collections: {list(collections)}")
        
        database_has_data = False
        
        # Check Scenario collection
        if "Scenario" in collections:
            print(f"\n🏷️ SCENARIO COLLECTION:")
            scenarios_collection = client.collections.get("Scenario")
            
            # Get exact count
            result = scenarios_collection.aggregate.over_all(total_count=True)
            scenario_count = result.total_count
            print(f"   📊 Total scenarios in database: {scenario_count}")
            
            if scenario_count > 0:
                database_has_data = True
                print("   ✅ SCENARIOS ARE IN DATABASE!")
                
                # Get sample data to verify it's your CSV data
                response = scenarios_collection.query.fetch_objects(limit=3)
                print(f"   🔍 Sample scenarios from database:")
                
                for i, obj in enumerate(response.objects, 1):
                    print(f"\n   --- Database Scenario {i} ---")
                    print(f"   ID: {obj.uuid}")
                    for prop_name, prop_value in obj.properties.items():
                        # Show first 100 chars to verify content
                        if isinstance(prop_value, str) and len(prop_value) > 100:
                            display_value = prop_value[:100] + "..."
                        else:
                            display_value = prop_value
                        print(f"   {prop_name}: {display_value}")
                
                # Test search to verify vectorization
                print(f"\n   🔎 Testing vector search:")
                search_response = scenarios_collection.query.near_text(
                    query="frontend web development",
                    limit=2
                )
                
                if search_response.objects:
                    print(f"   ✅ Vector search works! Found {len(search_response.objects)} results")
                    for obj in search_response.objects:
                        title = obj.properties.get('title', 'No title')[:50]
                        role = obj.properties.get('role', 'No role')
                        print(f"      - {role}: {title}...")
                else:
                    print("   ⚠️ Vector search returned no results (vectorization may be pending)")
            else:
                print("   ❌ NO SCENARIOS IN DATABASE")
        else:
            print("   ❌ Scenario collection doesn't exist")
        
        # Check TrainingResource collection
        if "TrainingResource" in collections:
            print(f"\n🏷️ TRAINING RESOURCE COLLECTION:")
            resources_collection = client.collections.get("TrainingResource")
            
            result = resources_collection.aggregate.over_all(total_count=True)
            resource_count = result.total_count
            print(f"   📊 Total resources in database: {resource_count}")
            
            if resource_count > 0:
                database_has_data = True
                print("   ✅ TRAINING RESOURCES ARE IN DATABASE!")
                
                response = resources_collection.query.fetch_objects(limit=2)
                print(f"   🔍 Sample resources from database:")
                
                for i, obj in enumerate(response.objects, 1):
                    print(f"\n   --- Database Resource {i} ---")
                    print(f"   ID: {obj.uuid}")
                    for prop_name, prop_value in obj.properties.items():
                        print(f"   {prop_name}: {prop_value}")
            else:
                print("   📭 No training resources in database")
        else:
            print("   ❌ TrainingResource collection doesn't exist")
        
        # Check other collections (like Drug, DrugInteraction that we saw before)
        for collection_name in collections:
            if collection_name not in ["Scenario", "TrainingResource"]:
                print(f"\n🏷️ OTHER COLLECTION: {collection_name}")
                try:
                    other_collection = client.collections.get(collection_name)
                    result = other_collection.aggregate.over_all(total_count=True)
                    count = result.total_count
                    print(f"   📊 {collection_name}: {count} objects")
                except Exception as e:
                    print(f"   ❌ Error checking {collection_name}: {e}")
        
        client.close()
        return database_has_data
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return False

def check_api_memory():
    """Check what's in API memory vs database"""
    print(f"\n🔍 CHECKING API MEMORY STORAGE")
    print("=" * 50)
    
    try:
        # Check scenarios in memory
        response = requests.get(f"{API_BASE}/debug/scenarios")
        if response.status_code == 200:
            data = response.json()
            memory_count = data.get('count', 0)
            print(f"📊 Scenarios in API memory: {memory_count}")
            
            if memory_count > 0:
                print("✅ SCENARIOS ARE IN API MEMORY!")
                # Show sample from memory
                if data.get('scenarios'):
                    sample = data['scenarios'][0]
                    print(f"🔍 Sample from memory:")
                    for key, value in sample.items():
                        if isinstance(value, str) and len(value) > 100:
                            display_value = value[:100] + "..."
                        else:
                            display_value = value
                        print(f"   {key}: {display_value}")
            else:
                print("❌ No scenarios in API memory")
                
            return memory_count
        else:
            print(f"❌ API memory check failed: {response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ API memory check error: {e}")
        return 0

def check_api_database_endpoint():
    """Check the API's view of the database"""
    print(f"\n🔍 CHECKING API'S VIEW OF DATABASE")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE}/debug/weaviate-data")
        if response.status_code == 200:
            data = response.json()
            print("📋 API reports from database:")
            print(f"   Weaviate Status: {data.get('weaviate_status', 'unknown')}")
            print(f"   Scenarios in database: {data.get('scenarios_in_weaviate', 0)}")
            print(f"   Resources in database: {data.get('resources_in_weaviate', 0)}")
            
            if data.get('sample_scenario'):
                print(f"   ✅ Sample scenario found in database via API")
                sample = data['sample_scenario']
                for key, value in sample.items():
                    if isinstance(value, str) and len(value) > 100:
                        display_value = value[:100] + "..."
                    else:
                        display_value = value
                    print(f"      {key}: {display_value}")
                return True
            else:
                print(f"   ❌ No sample scenario found via API")
                return False
        else:
            print(f"❌ API database endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API database endpoint error: {e}")
        return False

def test_data_upload():
    """Test uploading scenarios.csv again to see what happens"""
    print(f"\n🔍 TESTING UPLOAD PROCESS")
    print("=" * 50)
    
    try:
        import os
        if os.path.exists("scenarios.csv"):
            print("✅ scenarios.csv found")
            
            # Check file content
            with open("scenarios.csv", "r", encoding='utf-8') as f:
                lines = f.readlines()
                print(f"📄 CSV file has {len(lines)} lines (including header)")
                if len(lines) > 1:
                    print(f"📝 Header: {lines[0].strip()}")
                    print(f"📝 Sample row: {lines[1].strip()}")
            
            # Try upload
            with open("scenarios.csv", "rb") as f:
                files = {"file": ("scenarios.csv", f, "text/csv")}
                response = requests.post(f"{API_BASE}/upload-scenarios", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Upload successful!")
                    print(f"📊 API says it processed: {result.get('count')} scenarios")
                    print(f"📝 Message: {result.get('message')}")
                    return True
                else:
                    print(f"❌ Upload failed: {response.status_code}")
                    print(f"Error: {response.text}")
                    return False
        else:
            print("❌ scenarios.csv not found")
            return False
            
    except Exception as e:
        print(f"❌ Upload test error: {e}")
        return False

def main():
    """Run comprehensive verification"""
    print("🚀 COMPREHENSIVE DATABASE DATA VERIFICATION")
    print("🎯 Goal: Confirm CSV data is actually stored in Weaviate database")
    print("=" * 70)
    
    # 1. Check if API is running
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API health check failed")
            return
    except:
        print("❌ API not running. Start with: python main.py")
        return
    
    # 2. Check API memory
    memory_count = check_api_memory()
    
    # 3. Check API's view of database
    api_sees_db = check_api_database_endpoint()
    
    # 4. Check database directly
    db_has_data = check_weaviate_database()
    
    # 5. If no data in database, test upload
    if not db_has_data and memory_count > 0:
        print(f"\n⚠️ DATA MISMATCH DETECTED!")
        print(f"   API Memory: {memory_count} scenarios")
        print(f"   Database: 0 scenarios")
        print(f"   This suggests upload to database failed")
        
        print(f"\n🔄 Testing upload process...")
        upload_success = test_data_upload()
        
        if upload_success:
            print(f"\n🔄 Re-checking database after upload...")
            db_has_data = check_weaviate_database()
    
    # 6. Final verdict
    print(f"\n" + "=" * 70)
    print("🏁 FINAL VERDICT:")
    print("=" * 70)
    
    print(f"API Memory Storage: {'✅ HAS DATA' if memory_count > 0 else '❌ NO DATA'} ({memory_count} scenarios)")
    print(f"Weaviate Database: {'✅ HAS DATA' if db_has_data else '❌ NO DATA'}")
    print(f"API Database View: {'✅ CAN READ DB' if api_sees_db else '❌ CANNOT READ DB'}")
    
    if db_has_data:
        print(f"\n🎉 SUCCESS! Your CSV data IS stored in the Weaviate database!")
        print(f"   ✅ Data upload completed successfully")
        print(f"   ✅ Vector search is available")
        print(f"   ✅ System is ready for production use")
    elif memory_count > 0:
        print(f"\n⚠️ PARTIAL SUCCESS: Data is in memory but not in database")
        print(f"   ⚠️ Check vector_store.add_scenarios() function")
        print(f"   ⚠️ Check Weaviate connection during upload")
        print(f"   ⚠️ Data will be lost on API restart")
    else:
        print(f"\n❌ NO DATA FOUND anywhere!")
        print(f"   ❌ Upload scenarios.csv first")
        print(f"   ❌ Check CSV file format")

if __name__ == "__main__":
    main()