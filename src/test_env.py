from dotenv import load_dotenv
import os
import sys

def test_env():
    load_dotenv()
    
    print("Python Path:", sys.executable)
    print("\nEnvironment Variables:")
    print("-" * 40)
    
    # Check API credentials
    api_key = os.getenv('ANGLE_ONE_API_KEY')
    client_id = os.getenv('ANGLE_ONE_CLIENT_ID')
    password = os.getenv('ANGLE_ONE_PASSWORD')
    
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    print(f"Client ID present: {'Yes' if client_id else 'No'}")
    print(f"Password present: {'Yes' if password else 'No'}")
    
    print("\nInstalled Packages:")
    print("-" * 40)
    
    # List installed packages
    import pkg_resources
    installed_packages = [dist.project_name for dist in pkg_resources.working_set]
    print("\n".join(installed_packages))

if __name__ == "__main__":
    test_env()