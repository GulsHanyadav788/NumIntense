import requests
import time
import json
from colorama import Fore, Style, init
from typing import Dict, List, Optional

# Initialize colorama for colored output
init(autoreset=True)

class EmailBreachChecker:
    def __init__(self, hibp_api_key: str = None, user_agent: str = "NumIntensePro-OSINT-Tool/2.0"):
        """
        Initialize the breach checker with API key and user agent
        
        Args:
            hibp_api_key: Have I Been Pwned API key (optional but recommended)
            user_agent: Custom user agent string
        """
        self.hibp_api_key = hibp_api_key
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'application/vnd.haveibeenpwned.v3+json'
        })
        
        # Add API key if provided
        if self.hibp_api_key:
            self.session.headers['hibp-api-key'] = self.hibp_api_key
            
        self.rate_limit_delay = 1.6  # HIBP requires 1.5s between requests

    def check_hibp_breaches(self, email: str) -> Optional[Dict]:
        """
        Check email against Have I Been Pwned database
        
        Args:
            email: Email address to check
            
        Returns:
            Dictionary with breach data or None if error
        """
        print(Fore.YELLOW + f"\n[🔍] Checking Have I Been Pwned for: {email}")
        
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            params = {
                'truncateResponse': False  # Get full breach details
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            # Handle different status codes
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'status': 'found',
                    'breaches': breaches,
                    'count': len(breaches)
                }
                
            elif response.status_code == 404:
                return {
                    'status': 'not_found',
                    'breaches': [],
                    'count': 0
                }
                
            elif response.status_code == 429:  # Rate limited
                print(Fore.RED + "[!] Rate limited - waiting before retry...")
                time.sleep(10)  # Wait longer for rate limit
                return self.check_hibp_breaches(email)  # Retry once
                
            elif response.status_code == 401:  # Unauthorized
                return {
                    'status': 'error',
                    'error': 'Invalid API key or unauthorized'
                }
                
            else:
                return {
                    'status': 'error',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'status': 'error',
                'error': 'Request timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'status': 'error', 
                'error': 'Connection error'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': f"Unexpected error: {str(e)}"
            }

    def check_dehashed(self, email: str, api_key: str = None) -> Optional[Dict]:
        """
        Check email against DeHashed database (if API key available)
        
        Args:
            email: Email address to check
            api_key: DeHashed API key (optional)
            
        Returns:
            Dictionary with dehashed results or None
        """
        if not api_key:
            return None
            
        print(Fore.YELLOW + f"[🔍] Checking DeHashed for: {email}")
        
        try:
            url = "https://api.dehashed.com/search"
            params = {
                'query': f'email:"{email}"'
            }
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Basic {api_key}'
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'success',
                    'entries': data.get('entries', []),
                    'total': data.get('total', 0)
                }
            else:
                return {
                    'status': 'error',
                    'error': f"DeHashed API error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': f"DeHashed check failed: {str(e)}"
            }

    def format_breach_info(self, breach: Dict) -> str:
        """Format individual breach information"""
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

    def display_results(self, email: str, hibp_result: Dict, dehashed_result: Dict = None):
        """Display formatted results"""
        print(Fore.CYAN + f"\n{'='*60}")
        print(Fore.CYAN + f"📧 EMAIL BREACH REPORT: {email}")
        print(Fore.CYAN + f"{'='*60}")
        
        # HIBP Results
        if hibp_result['status'] == 'found':
            print(Fore.RED + f"\n[⚠️] HAVE I BEEN PWNED: {hibp_result['count']} breaches found!")
            
            for i, breach in enumerate(hibp_result['breaches'], 1):
                print(Fore.YELLOW + f"\n[{i}/{hibp_result['count']}]" + self.format_breach_info(breach))
                
        elif hibp_result['status'] == 'not_found':
            print(Fore.GREEN + "\n[✓] HAVE I BEEN PWNED: No breaches found!")
            
        elif hibp_result['status'] == 'error':
            print(Fore.RED + f"\n[❌] HAVE I BEEN PWNED ERROR: {hibp_result['error']}")
            
        # DeHashed Results
        if dehashed_result and dehashed_result['status'] == 'success':
            if dehashed_result['total'] > 0:
                print(Fore.RED + f"\n[⚠️] DEHASHED: {dehashed_result['total']} records found!")
                # Display first few entries
                for entry in dehashed_result['entries'][:3]:  # Show first 3
                    print(Fore.YELLOW + f"  └─ {entry.get('email')} | {entry.get('password', 'N/A')}")
                if dehashed_result['total'] > 3:
                    print(Fore.YELLOW + f"  └─ ... and {dehashed_result['total'] - 3} more entries")
            else:
                print(Fore.GREEN + "\n[✓] DEHASHED: No records found!")
                
        elif dehashed_result and dehashed_result['status'] == 'error':
            print(Fore.RED + f"\n[❌] DEHASHED ERROR: {dehashed_result['error']}")

    def email_breach_check(self, email: str, dehashed_api_key: str = None) -> bool:
        """
        Comprehensive email breach check
        
        Args:
            email: Email address to check
            dehashed_api_key: DeHashed API key (optional)
            
        Returns:
            Boolean indicating if breaches were found
        """
        print(Fore.CYAN + f"\n[🛡️] Starting comprehensive breach check for: {email}")
        
        # Validate email format
        if not self.validate_email(email):
            print(Fore.RED + "[❌] Invalid email format")
            return False
        
        try:
            # Check HIBP
            hibp_result = self.check_hibp_breaches(email)
            
            # Respect rate limiting
            time.sleep(self.rate_limit_delay)
            
            # Check DeHashed if API key provided
            dehashed_result = None
            if dehashed_api_key:
                dehashed_result = self.check_dehashed(email, dehashed_api_key)
            
            # Display results
            self.display_results(email, hibp_result, dehashed_result)
            
            # Return True if any breaches found
            breaches_found = (
                hibp_result.get('count', 0) > 0 or
                (dehashed_result and dehashed_result.get('total', 0) > 0)
            )
            
            if breaches_found:
                print(Fore.RED + f"\n[💀] SUMMARY: Breaches found for {email}!")
                self.generate_recommendations()
            else:
                print(Fore.GREEN + f"\n[✅] SUMMARY: No breaches found for {email}")
                
            return breaches_found
            
        except Exception as e:
            print(Fore.RED + f"[❌] Unexpected error during breach check: {str(e)}")
            return False

    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def generate_recommendations(self):
        """Generate security recommendations"""
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

    def batch_check_emails(self, emails: List[str], delay: float = 2.0):
        """
        Check multiple emails with rate limiting
        
        Args:
            emails: List of email addresses
            delay: Delay between requests in seconds
        """
        print(Fore.CYAN + f"\n[🔍] Starting batch check for {len(emails)} emails...")
        
        results = {}
        for email in emails:
            if self.validate_email(email):
                found = self.email_breach_check(email)
                results[email] = found
                time.sleep(delay)
            else:
                print(Fore.RED + f"[❌] Skipping invalid email: {email}")
                results[email] = False
                
        return results


# Simplified function for basic usage (backward compatibility)
def email_breach_check(email: str, hibp_api_key: str = None) -> bool:
    """
    Simplified breach check function (backward compatible)
    
    Args:
        email: Email address to check
        hibp_api_key: HIBP API key (optional)
        
    Returns:
        Boolean indicating if breaches were found
    """
    checker = EmailBreachChecker(hibp_api_key)
    return checker.email_breach_check(email)


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    checker = EmailBreachChecker(hibp_api_key="YOUR_API_KEY_HERE")
    
    # Single email check
    checker.email_breach_check("test@example.com")
    
    # Batch check
    emails = ["user1@example.com", "user2@example.com"]
    checker.batch_check_emails(emails)
    
    # Or use simplified function
    email_breach_check("test@example.com")