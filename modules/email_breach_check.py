# Enhanced Email Breach Check Module
import requests
import time
import json
from colorama import Fore, Style, init
from typing import Dict, List, Optional

init(autoreset=True)

class EmailBreachChecker:
    def __init__(self, hibp_api_key: str = None, user_agent: str = "NumIntensePro-OSINT-Tool/2.0"):
        self.hibp_api_key = hibp_api_key
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'application/vnd.haveibeenpwned.v3+json'
        })
        
        if self.hibp_api_key:
            self.session.headers['hibp-api-key'] = self.hibp_api_key
            
        self.rate_limit_delay = 1.6

    def check_hibp_breaches(self, email: str) -> Optional[Dict]:
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            params = {'truncateResponse': False}
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'status': 'found',
                    'breaches': breaches,
                    'count': len(breaches)
                }
            elif response.status_code == 404:
                return {'status': 'not_found', 'breaches': [], 'count': 0}
            elif response.status_code == 429:
                print(Fore.RED + "[!] Rate limited - waiting before retry...")
                time.sleep(10)
                return self.check_hibp_breaches(email)
            elif response.status_code == 401:
                return {'status': 'error', 'error': 'Invalid API key'}
            else:
                return {'status': 'error', 'error': f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def format_breach_info(self, breach: Dict) -> str:
        name = breach.get('Name', 'Unknown')
        title = breach.get('Title', name)
        domain = breach.get('Domain', 'N/A')
        breach_date = breach.get('BreachDate', 'Unknown')
        added_date = breach.get('AddedDate', 'Unknown')
        pwn_count = breach.get('PwnCount', 0)
        data_classes = ', '.join(breach.get('DataClasses', []))
        
        info = f"""
{Fore.RED}┌─ Breach: {title}
{Fore.RED}├─ Domain: {domain}
{Fore.RED}├─ Date: {breach_date} (Added: {added_date})
{Fore.RED}├─ Records: {pwn_count:,}
{Fore.RED}└─ Data Compromised: {data_classes}"""
        
        return info

    def display_results(self, email: str, hibp_result: Dict):
        print(Fore.CYAN + f"\n{'='*60}")
        print(Fore.CYAN + f"📧 EMAIL BREACH REPORT: {email}")
        print(Fore.CYAN + f"{'='*60}")
        
        if hibp_result['status'] == 'found':
            print(Fore.RED + f"\n[⚠️] HAVE I BEEN PWNED: {hibp_result['count']} breaches found!")
            for i, breach in enumerate(hibp_result['breaches'], 1):
                print(Fore.YELLOW + f"\n[{i}/{hibp_result['count']}]" + self.format_breach_info(breach))
        elif hibp_result['status'] == 'not_found':
            print(Fore.GREEN + "\n[✓] HAVE I BEEN PWNED: No breaches found!")
        elif hibp_result['status'] == 'error':
            print(Fore.RED + f"\n[❌] HAVE I BEEN PWNED ERROR: {hibp_result['error']}")

    def email_breach_check(self, email: str) -> bool:
        print(Fore.CYAN + f"\n[🛡️] Starting breach check for: {email}")
        
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            print(Fore.RED + "[❌] Invalid email format")
            return False
        
        try:
            hibp_result = self.check_hibp_breaches(email)
            time.sleep(self.rate_limit_delay)
            
            self.display_results(email, hibp_result)
            
            breaches_found = hibp_result.get('count', 0) > 0
            if breaches_found:
                print(Fore.RED + f"\n[💀] SUMMARY: Breaches found for {email}!")
                self.generate_recommendations()
            else:
                print(Fore.GREEN + f"\n[✅] SUMMARY: No breaches found for {email}")
                
            return breaches_found
            
        except Exception as e:
            print(Fore.RED + f"[❌] Unexpected error: {str(e)}")
            return False

    def generate_recommendations(self):
        print(Fore.YELLOW + "\n[💡] SECURITY RECOMMENDATIONS:")
        recommendations = [
            "Change password immediately if reused across sites",
            "Enable two-factor authentication (2FA)",
            "Use a password manager for unique passwords",
            "Monitor accounts for suspicious activity",
            "Consider using breach monitoring services"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print(Fore.YELLOW + f"  {i}. {rec}")

# Simplified function for basic usage
def email_breach_check(email: str, hibp_api_key: str = None) -> bool:
    checker = EmailBreachChecker(hibp_api_key)
    return checker.email_breach_check(email)