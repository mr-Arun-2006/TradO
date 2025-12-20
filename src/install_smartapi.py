import os
import requests
import zipfile
import io
import shutil

def download_and_install_smartapi():
    # Download URL for the package
    url = "https://codeload.github.com/angelbroking-github/smartapi-python/zip/refs/heads/main"
    
    try:
        print("Downloading SmartAPI package...")
        response = requests.get(url)
        
        if response.status_code == 200:
            # Extract the zip file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(".")
                
            print("Package downloaded and extracted successfully")
            
            # Move to the extracted directory and install
            os.chdir("smartapi-python-main")
            os.system("..\.venv\Scripts\pip install .")
            os.chdir("..")
            
            # Clean up
            shutil.rmtree("smartapi-python-main")
            print("Installation completed")
            return True
        else:
            print(f"Failed to download package: Status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error during installation: {str(e)}")
        return False

if __name__ == "__main__":
    download_and_install_smartapi()