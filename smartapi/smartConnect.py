import requests
import json
import datetime
import websocket

class SmartConnect(object):
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://apiconnect.angelbroking.com"
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.debug_mode = False
        
    def enable_debug(self, enable=True):
        """Enable debug mode for detailed error information"""
        self.debug_mode = enable
        
    def _validate_credentials(self):
        """Validate credential format before making API calls"""
        errors = []
        
        if not self.api_key:
            errors.append("API Key is missing")
        elif len(self.api_key) < 20:
            errors.append("API Key appears to be invalid (too short)")
            
        return errors
        
    def _prepare_headers(self, include_token=False):
        """Prepare request headers with proper format"""
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-PrivateKey': self.api_key
        }
        
        if include_token and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
            
        return headers
        
    def _handle_response(self, response, action="API call"):
        """Handle API response with proper error handling"""
        try:
            data = response.json() if response.content else {}
            
            if response.status_code == 200:
                if data.get('status'):
                    return {
                        "status": True,
                        "data": data.get('data', {}),
                        "message": data.get('message', 'Success')
                    }
                else:
                    return {
                        "status": False,
                        "error_code": "API_ERROR",
                        "message": data.get('message', 'API returned failure'),
                        "debug_info": data if self.debug_mode else None
                    }
            elif response.status_code == 401:
                return {
                    "status": False,
                    "error_code": "UNAUTHORIZED",
                    "message": "Invalid credentials or token expired",
                    "debug_info": data if self.debug_mode else None
                }
            elif response.status_code == 403:
                return {
                    "status": False,
                    "error_code": "FORBIDDEN",
                    "message": "IP not whitelisted or access denied",
                    "debug_info": data if self.debug_mode else None
                }
            elif response.status_code == 400:
                return {
                    "status": False,
                    "error_code": "BAD_REQUEST",
                    "message": "Invalid request format or parameters",
                    "debug_info": data if self.debug_mode else None
                }
            else:
                return {
                    "status": False,
                    "error_code": f"HTTP_{response.status_code}",
                    "message": f"Unexpected response: {response.status_code}",
                    "debug_info": data if self.debug_mode else None
                }
                
        except ValueError as e:
            return {
                "status": False,
                "error_code": "INVALID_RESPONSE",
                "message": f"Failed to parse response: {str(e)}",
                "debug_info": {"response_text": response.text} if self.debug_mode else None
            }
        
    def generateSession(self, client_code, password):
        """Generate a new session with enhanced error handling"""
        try:
            if not self.api_key:
                return {
                    "status": False,
                    "message": "API Key is missing. Please check your credentials.",
                    "error_code": "NO_API_KEY"
                }
                
            if not client_code or not password:
                return {
                    "status": False,
                    "message": "Client code or password is missing",
                    "error_code": "INVALID_CREDENTIALS"
                }
                
            params = {
                "clientcode": client_code,
                "password": password
            }
            
            headers = {
                'Content-type': 'application/json',
                'X-PrivateKey': self.api_key,
                'Accept': 'application/json'
            }
            
            url = f"{self.base_url}/rest/auth/angelbroking/user/v1/loginByPassword"
            
            try:
                response = self.session.post(url, json=params, headers=headers)
                response.raise_for_status()  # Raise exception for non-200 status codes
                
                data = response.json()
                
                if data.get('status'):
                    self.access_token = data.get('data', {}).get('jwtToken')
                    self.refresh_token = data.get('data', {}).get('refreshToken')
                    
                    if not self.access_token:
                        return {
                            "status": False,
                            "message": "No access token in response",
                            "error_code": "NO_TOKEN",
                            "response": data
                        }
                        
                    return {
                        "status": True,
                        "data": data.get('data', {}),
                        "message": "Successfully logged in"
                    }
                else:
                    return {
                        "status": False,
                        "message": data.get('message', 'Login failed'),
                        "error_code": "LOGIN_FAILED",
                        "response": data
                    }
                    
            except requests.exceptions.RequestException as e:
                return {
                    "status": False,
                    "message": f"Network error: {str(e)}",
                    "error_code": "NETWORK_ERROR"
                }
                
        except Exception as e:
            return {
                "status": False,
                "message": f"Unexpected error: {str(e)}",
                "error_code": "UNKNOWN_ERROR"
            }
            
    def getProfile(self):
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-type': 'application/json',
                'X-PrivateKey': self.api_key
            }
            
            url = f"{self.base_url}/rest/secure/angelbroking/user/v1/getProfile"
            response = self.session.get(url, headers=headers)
            
            return response.json()
            
        except Exception as e:
            return {"status": False, "message": str(e)}
            
    def ltpData(self, exchange, tradingsymbol, symboltoken):
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-type': 'application/json',
                'X-PrivateKey': self.api_key
            }
            
            params = {
                "exchange": exchange,
                "tradingsymbol": tradingsymbol,
                "symboltoken": symboltoken
            }
            
            url = f"{self.base_url}/rest/secure/angelbroking/order/v1/getLtpData"
            response = self.session.post(url, json=params, headers=headers)
            
            return response.json()
            
        except Exception as e:
            return {"status": False, "message": str(e)}