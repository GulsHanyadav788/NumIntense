# NumVerify API Integration
import requests
import json
from colorama import Fore, Style

class NumVerifyAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://apilayer.net/api/validate"
    
    def validate_number(self, number):
        """Validate phone number using NumVerify API"""
        try:
            params = {
                'access_key': self.api_key,
                'number': number,
                'format': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('valid'):
                return {
                    'valid': True,
                    'number': data.get('international_format'),
                    'local_format': data.get('local_format'),
                    'country': data.get('country_name'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type'),
                    'location': data.get('location')
                }
            else:
                return {'valid': False, 'error': 'Invalid number'}
                
        except Exception as e:
            return {'valid': False, 'error': str(e)}