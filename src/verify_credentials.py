from dotenv import load_dotenv
import os
import requests
import json

def verify_credentials():
    load_dotenv()
    
    print("🔍 Verifying Angel One Credentials...")
    print("-" * 50)
    
    # Get credentials
    api_key = os.getenv('ANGLE_ONE_API_KEY')
    client_id = os.getenv('ANGLE_ONE_CLIENT_ID')
    password = os.getenv('ANGLE_ONE_PASSWORD')
    
    # Check if credentials exist
    credentials_status = {
        'API Key': bool(api_key),
        'Client ID': bool(client_id),
        'Password': bool(password)
    }
    
    print("\n1. Checking if credentials are present:")
    for cred, exists in credentials_status.items():
        print(f"   {'✅' if exists else '❌'} {cred}: {'Present' if exists else 'Missing'}")
    
    if not all(credentials_status.values()):
        print("\n❌ Error: Some credentials are missing in .env file")
        return False
    
    print("\n2. Validating API Key format:")
    if len(api_key) < 20:  # Angel One API keys are typically longer
        print("❌ API Key seems too short - might be invalid")
    else:
        print("✅ API Key length seems valid")
    
    print("\n3. Testing API Endpoint Connection:")
    try:
        headers = {
            'X-PrivateKey': api_key,
            'Accept': 'application/json',
            'X-ClientCode': client_id,
            'Content-Type': 'application/json'
        }
        
        # Test connection with login endpoint
        url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
        payload = {
            "clientcode": client_id,
            "password": password
        }
        
        print("   Attempting to connect to Angel One API...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"   Response Status Code: {response.status_code}")
        print(f"   Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response Data: {json.dumps(data, indent=2)}")
            if data.get('status'):
                print("\n✅ API Connection Successful!")
                print("🔑 Successfully authenticated with Angel One")
                return True
            else:
                print(f"\n❌ Authentication Failed: {data.get('message', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ Connection Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    verify_credentials()