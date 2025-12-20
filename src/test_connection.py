from smartapi import SmartConnect
from dotenv import load_dotenv
import os

def test_connection():
    load_dotenv()
    
    # Get credentials from .env
    api_key = os.getenv('ANGLE_ONE_API_KEY')
    client_id = os.getenv('ANGLE_ONE_CLIENT_ID')
    password = os.getenv('ANGLE_ONE_PASSWORD')
    
    print("Testing Angel One Smart API Connection...")
    print(f"Client ID: {client_id}")
    
    try:
        # Initialize
        smart_api = SmartConnect(api_key=api_key)
        
        # Generate session
        data = smart_api.generateSession(client_id, password)
        
        if data['status']:
            print("\n✅ Connection Successful!")
            print("Access Token Generated:", data['data']['jwt'][:10] + "..." if data['data']['jwt'] else "None")
            print("\nAccount Details:")
            print("-" * 40)
            
            # Get user profile
            profile = smart_api.getProfile()
            if profile['status']:
                profile_data = profile['data']
                print(f"Name: {profile_data.get('name', 'N/A')}")
                print(f"Email: {profile_data.get('email', 'N/A')}")
                print(f"Account Type: {profile_data.get('accountType', 'N/A')}")
                print(f"Broker: {profile_data.get('broker', 'N/A')}")
                
                # Test market data access
                print("\nTesting Market Data Access:")
                print("-" * 40)
                try:
                    nifty_data = smart_api.ltpData("NSE", "NIFTY", "INDEX")
                    if nifty_data['status']:
                        print(f"NIFTY Current Price: {nifty_data['data']['ltp']}")
                    else:
                        print("Could not fetch NIFTY data")
                except Exception as e:
                    print(f"Market data error: {str(e)}")
            else:
                print("Could not fetch profile details")
        else:
            print("\n❌ Connection Failed!")
            print(f"Error: {data.get('message', 'Unknown error')}")
            
    except Exception as e:
        print("\n❌ Connection Error!")
        print(f"Error details: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your API key is correct")
        print("2. Verify your Client ID and password")
        print("3. Make sure your IP is whitelisted in Angel One dashboard")
        print("4. Check if your account has API trading enabled")

if __name__ == "__main__":
    test_connection()