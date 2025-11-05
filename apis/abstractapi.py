# AbstractAPI Integration
import requests
from colorama import Fore

class AbstractAPI:
    def __init__(self, api_key):
        self.api_key = Key:efd9c38411b1492ab17c244c0305c286
        self.base_url = "https://phonevalidation.abstractapi.com/v1/"
    
    def validate_number(self, number):
        try:
            params = {
                'api_key': self.api_key,
                'phone': number
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            return data
            
        except Exception as e:
            return {'error': str(e)}