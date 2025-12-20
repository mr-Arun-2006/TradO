from smartapi import SmartConnect
from dotenv import load_dotenv
import os

def test_smartapi():
    load_dotenv()
    
    print("Testing SmartAPI connection...")
    api_key = os.getenv('ANGLE_ONE_API_KEY')
    client_id = os.getenv('ANGLE_ONE_CLIENT_ID')
    password = os.getenv('ANGLE_ONE_PASSWORD')
    
    try:
        # Initialize
        smart_api = SmartConnect(api_key=api_key)
        print("✅ SmartAPI initialized successfully")
        
        # Try to login
        session = smart_api.generateSession(client_id, password)
        if session and session.get('status'):
            print("✅ Login successful!")
            print("\nTrying to get profile info...")
            profile = smart_api.getProfile()
            if profile and profile.get('status'):
                print("✅ Profile data retrieved successfully")
                print("\nProfile Details:")
                print("-" * 40)
                print(f"Name: {profile['data'].get('name', 'N/A')}")
                print(f"Email: {profile['data'].get('email', 'N/A')}")
            else:
                print("❌ Could not retrieve profile")
        else:
            print(f"❌ Login failed: {session.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_smartapi()