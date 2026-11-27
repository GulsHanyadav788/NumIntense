#!/usr/bin/env python3
"""
Secure API Handler
Description: Safe API integrations with config management
Version: 3.1.0
"""

import requests
import json
import os
from colorama import Fore, Style

class SecureAPI:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.session = requests.Session()
        
    def load_config(self):
        """Safely load configuration"""
        default_config = {
            "api_keys": {
                "numverify": "",
                "abstractapi": "",
                "hibp": ""
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    if "api_keys" in user_config:
                        default_config["api_keys"].update(user_config["api_keys"])
            return default_config
        except:
            return default_config
            
    def get_api_key(self, service):
        """Safely get API key from config"""
        return self.config["api_keys"].get(service, "")
        
    def test_connection(self):
        """Test internet connection"""
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return True
        except:
            return False

class PhoneAPI(SecureAPI):
    """Phone number API services"""
    
    def numverify_lookup(self, number):
        """NumVerify API lookup"""
        api_key = self.get_api_key("numverify")
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            return {"error": "NumVerify API key not configured"}
            
        try:
            url = "http://apilayer.net/api/validate"
            params = {
                'access_key': api_key,
                'number': number,
                'format': 1
            }
            
            response = self.session.get(url, params=params, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def abstractapi_lookup(self, number):
        """AbstractAPI phone validation"""
        api_key = self.get_api_key("abstractapi")
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            return {"error": "AbstractAPI key not configured"}
            
        try:
            url = "https://phonevalidation.abstractapi.com/v1/"
            params = {
                'api_key': api_key,
                'phone': number
            }
            
            response = self.session.get(url, params=params, timeout=10)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class EmailAPI(SecureAPI):
    """Email API services"""
    
    def hibp_check(self, email):
        """Have I Been Pwned API check"""
        api_key = self.get_api_key("hibp")
        
        try:
            headers = {}
            if api_key and api_key != "YOUR_API_KEY_HERE":
                headers['hibp-api-key'] = api_key
                
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            response = self.session.get(url, headers=headers, timeout=10, params={'truncateResponse': False})
            
            if response.status_code == 200:
                return {"breaches": response.json(), "count": len(response.json())}
            elif response.status_code == 404:
                return {"breaches": [], "count": 0}
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}