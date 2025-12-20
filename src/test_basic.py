import requests
import os
from dotenv import load_dotenv

def test_credentials():
    load_dotenv()
    
    print("Testing API Credentials...")
    
    api_key = os.getenv('ANGLE_ONE_API_KEY')
    client_id = os.getenv('ANGLE_ONE_CLIENT_ID')
    
    if not api_key or not client_id:
        print("❌ Error: Missing API credentials in .env file")
        return False
        
    # Test basic connectivity to Angel One's API endpoint
    try:
        response = requests.get('https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getProfile',
                              headers={'X-PrivateKey': api_key,
                                     'Accept': 'application/json',
                                     'X-ClientCode': client_id,
                                     'X-UserType': 'USER'})
        
        if response.status_code == 401:
            print("✅ API endpoint reached (Got expected 401 - needs login)")
            print("Your credentials exist and the API endpoint is accessible.")
            print("\nNext steps:")
            print("1. Install SmartAPI package from GitHub")
            print("2. Initialize proper session with login")
            return True
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_credentials()