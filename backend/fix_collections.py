#!/usr/bin/env python3
"""
Fix existing collections by deleting and recreating them
This removes the OpenAI vectorizer requirement
"""

import weaviate
from weaviate.auth import AuthApiKey

# Your configuration  
WEAVIATE_URL = "https://kaf6l0nwryaswmhnv6gq.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "MnBmdk1XZnNmTlREa01lUV94UTF3VkljTURVZExJZW90dmNzV0YvampWbnNJOVRROHhvWmh0czJKL2gwPV92MjAw"
GOOGLE_API_KEY = "AIzaSyA49dCXQSsZJMvDOsDCQrHZrBZZ2_HDQf4"

def fix_collections():
    """Delete and recreate collections properly"""
    print("🔧 Fixing Weaviate collections...")
    
    try:
        # Connect to Weaviate
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=AuthApiKey(WEAVIATE_API_KEY)
        )
        
        if not client.is_ready():
            print("❌ Cannot connect to Weaviate")
            return False
        
        print("✅ Connected to Weaviate")
        
        # Check existing collections
        existing_collections = client.collections.list_all()
        print(f"📋 Existing collections: {list(existing_collections)}")
        
        # Delete problematic collections
        collections_to_fix = ["Scenario", "TrainingResource"]
        
        for collection_name in collections_to_fix:
            if collection_name in existing_collections:
                print(f"🗑️ Deleting {collection_name} collection...")
                client.collections.delete(collection_name)
                print(f"✅ Deleted {collection_name}")
            else:
                print(f"ℹ️ {collection_name} doesn't exist")
        
        print("\n🏗️ Creating new collections without vectorizer...")
        
        # Create Scenario collection WITHOUT vectorizer
        client.collections.create(
            name="Scenario",
            description="Job scenarios for students",  
            properties=[
                weaviate.classes.config.Property(
                    name="role", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="title", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="task", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="difficulty", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="context", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
            ]
            # NO vectorizer_config - this prevents OpenAI API key requirement
        )
        print("✅ Created Scenario collection (no vectorizer)")
        
        # Create TrainingResource collection WITHOUT vectorizer
        client.collections.create(
            name="TrainingResource",
            description="Training resources for students",
            properties=[
                weaviate.classes.config.Property(
                    name="title", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="type", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="description", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="url", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
                weaviate.classes.config.Property(
                    name="skills", 
                    data_type=weaviate.classes.config.DataType.TEXT
                ),
            ]
            # NO vectorizer_config - this prevents OpenAI API key requirement
        )
        print("✅ Created TrainingResource collection (no vectorizer)")
        
        # Test insertion
        print("\n🧪 Testing data insertion...")
        
        scenario_collection = client.collections.get("Scenario")
        test_scenario = {
            "role": "test",
            "title": "Test Scenario", 
            "task": "This is a test scenario",
            "difficulty": "beginner",
            "context": "Testing context"
        }
        
        # Try inserting test object
        result = scenario_collection.data.insert(test_scenario)
        print(f"✅ Test insertion successful! Object ID: {result}")
        
        # Clean up test object
        scenario_collection.data.delete_by_id(result)
        print("🧹 Test object removed")
        
        # Verify collections exist
        new_collections = client.collections.list_all()
        print(f"📋 New collections: {list(new_collections)}")
        
        client.close()
        print("\n🎉 SUCCESS! Collections fixed. Data uploads will now work.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix collections: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_weaviate_client():
    """Show the updated weaviate_client.py content"""
    print("\n📝 Update your database/weaviate_client.py:")
    print("=" * 50)
    
    updated_code = '''
import weaviate
from weaviate.classes.init import Auth
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class WeaviateClient:
    def __init__(self):
        self.client = None
        self.connect()
    
    def connect(self):
        try:
            auth_config = Auth.api_key(settings.weaviate_api_key)
            
            self.client = weaviate.connect_to_weaviate_cloud(
                cluster_url=settings.weaviate_url,
                auth_credentials=auth_config
            )
            
            logger.info("Connected to Weaviate Cloud successfully")
            
            if self.client.is_ready():
                logger.info("Weaviate Cloud is ready")
            else:
                logger.warning("Weaviate Cloud connection established but not ready")
                
        except Exception as e:
            logger.error(f"Failed to connect to Weaviate Cloud: {e}")
            raise
    
    def create_schema(self):
        # Collections are now created without vectorizer
        # No schema creation needed - collections already exist
        logger.info("Schema already exists - no creation needed")
    
    def close(self):
        if self.client:
            self.client.close()

weaviate_client = WeaviateClient()
'''
    
    print(updated_code)

if __name__ == "__main__":
    print("🚀 FIXING WEAVIATE COLLECTIONS")
    print("=" * 60)
    
    success = fix_collections()
    
    if success:
        print("\n📋 NEXT STEPS:")
        print("1. Collections are now fixed")
        print("2. Restart your API: python main.py") 
        print("3. Upload CSV: curl -X POST -F 'file=@scenarios.csv' http://localhost:8000/upload-scenarios")
        print("4. Verify: curl http://localhost:8000/debug/weaviate-data")
        
        update_weaviate_client()
    else:
        print("\n❌ Fix failed. Check the error messages above.")