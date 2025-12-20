from smartapi import SmartConnect
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("Initializing Smart API connection...")
    api_key = os.getenv('ANGLE_ONE_API_KEY')
    
    try:
        smart_api = SmartConnect(api_key=api_key)
        print("✅ Successfully initialized Smart API")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    main()