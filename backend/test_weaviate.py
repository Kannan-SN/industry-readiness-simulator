#!/usr/bin/env python3
"""
Simple Weaviate Database Explorer
Save this as: test_weaviate.py
Run with: python test_weaviate.py
"""

import weaviate
import json

# Your Weaviate configuration
WEAVIATE_URL = "https://6y3tmu8jt6gyusexstfoa.c0.asia-southeast1.gcp.weaviate.cloud"
WEAVIATE_API_KEY = "SkNCaWVyM3pjU0dNT0x5L19XQXdaNHd2c2l4bVo3UmtMZ2hKdE1ucEJXK2NYL3VMb1NBbDJkcjJaN2JjPV92MjAw"

def quick_explore():
    """Quick exploration of your Weaviate database"""
    
    print("🚀 Connecting to Weaviate...")
    
    try:
        # Connect to Weaviate
        client = weaviate.Client(
            url=WEAVIATE_URL,
            auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
        )
        
        # Test connection
        if client.is_ready():
            print("✅ Connected successfully!")
        else:
            print("❌ Connection failed!")
            return
        
        # Get schema
        print("\n📋 Getting database schema...")
        schema = client.schema.get()
        
        if 'classes' in schema and schema['classes']:
            print(f"✅ Found {len(schema['classes'])} classes in your database:")
            
            for class_info in schema['classes']:
                class_name = class_info['class']
                print(f"\n🏷️  Class: {class_name}")
                
                # Get object count
                try:
                    result = client.query.aggregate(class_name).with_meta_count().do()
                    count = result['data']['Aggregate'][class_name][0]['meta']['count']
                    print(f"   📊 Objects: {count}")
                except Exception as e:
                    print(f"   ❌ Count error: {e}")
                
                # Show properties
                if 'properties' in class_info:
                    props = [prop['name'] for prop in class_info['properties']]
                    print(f"   📝 Properties: {', '.join(props[:5])}")  # Show first 5
                    if len(props) > 5:
                        print(f"       ... and {len(props) - 5} more")
                
                # Get sample data
                try:
                    result = client.query.get(class_name).with_limit(2).do()
                    objects = result['data']['Get'][class_name]
                    
                    if objects:
                        print(f"   🔍 Sample data:")
                        for i, obj in enumerate(objects, 1):
                            print(f"      Sample {i}:")
                            for key, value in obj.items():
                                if not key.startswith('_'):
                                    # Truncate long values
                                    if isinstance(value, str) and len(value) > 50:
                                        value = value[:50] + "..."
                                    print(f"        {key}: {value}")
                    else:
                        print("   📭 No objects found")
                        
                except Exception as e:
                    print(f"   ❌ Sample data error: {e}")
                
                print("-" * 40)
        else:
            print("❌ No classes found in your database!")
            print("   Your database might be empty or there might be a connection issue.")
        
        # Close connection
        client.close()
        print("\n✅ Exploration complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify your Weaviate URL and API key")
        print("3. Make sure weaviate-client is installed: pip install weaviate-client")

if __name__ == "__main__":
    quick_explore()