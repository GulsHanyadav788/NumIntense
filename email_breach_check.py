#!/usr/bin/env python3
"""
Email Intelligence Module
Description: Email breach checking and analysis
Version: 3.1.0
"""

import requests
import re
from colorama import Fore, Style, init

init(autoreset=True)

class EmailIntelligence:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })

    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def check_breaches(self, email):
        """Check email breaches"""
        print(Fore.CYAN + f"\n[📧] Email Intelligence: {email}")
        print(Fore.CYAN + "─" * 50)
        
        # Have I Been Pwned
        print(f"{Fore.YELLOW}[1] {Fore.WHITE}Have I Been Pwned:")
        print(f"    {Fore.CYAN}https://haveibeenpwned.com/account/{email}")
        
        # Dehashed (alternative)
        print(f"{Fore.YELLOW}[2] {Fore.WHITE}Dehashed Search:")
        print(f"    {Fore.CYAN}https://dehashed.com/search?query={email}")
        
        # BreachDirectory
        print(f"{Fore.YELLOW}[3] {Fore.WHITE}BreachDirectory:")
        print(f"    {Fore.CYAN}https://breachdirectory.org/?q={email}")

    def social_media_search(self, email):
        """Generate social media search links"""
        print(f"\n{Fore.YELLOW}[🔍] Social Media Search:")
        
        platforms = {
            "Facebook": f"https://www.facebook.com/search/top/?q={email}",
            "Instagram": f"https://www.instagram.com/search/top/?q={email}",
            "Twitter": f"https://twitter.com/search?q={email}",
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={email}",
            "Google": f"https://www.google.com/search?q={email}",
        }
        
        for platform, url in platforms.items():
            print(f"    {Fore.GREEN}• {platform}: {Fore.CYAN}{url}")

    def generate_dorks(self, email):
        """Generate Google dorks for email"""
        print(f"\n{Fore.YELLOW}[🎯] Google Dorks:")
        
        dorks = [
            f'intext:"{email}"',
            f'site:facebook.com "{email}"',
            f'site:twitter.com "{email}"',
            f'site:linkedin.com "{email}"',
            f'filetype:pdf "{email}"',
            f'"{email}" "password"',
            f'"{email}" "confidential"',
        ]
        
        for i, dork in enumerate(dorks, 1):
            encoded = requests.utils.quote(dork)
            url = f"https://www.google.com/search?q={encoded}"
            print(f"    {Fore.GREEN}[{i}] {Fore.WHITE}{dork}")
            print(f"        {Fore.CYAN}{url}")

    def domain_analysis(self, email):
        """Analyze email domain"""
        domain = email.split('@')[-1]
        print(f"\n{Fore.YELLOW}[🌐] Domain Analysis: {domain}")
        
        checks = {
            "WHOIS Lookup": f"https://whois.domaintools.com/{domain}",
            "Security Headers": f"https://securityheaders.com/?q={domain}",
            "SSL Labs": f"https://www.ssllabs.com/ssltest/analyze.html?d={domain}",
            "MX Tools": f"https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{domain}",
        }
        
        for check, url in checks.items():
            print(f"    {Fore.GREEN}• {check}: {Fore.CYAN}{url}")

    def full_scan(self, email):
        """Complete email intelligence scan"""
        if not self.validate_email(email):
            print(Fore.RED + "[❌] Invalid email format")
            return False
            
        print(Fore.CYAN + f"\n[🚀] Starting comprehensive email analysis...")
        
        self.check_breaches(email)
        self.social_media_search(email)
        self.generate_dorks(email)
        self.domain_analysis(email)
        
        print(f"\n{Fore.GREEN}[✅] Email analysis completed!")
        return True

def run_email_check(email):
    """Main function to run email check"""
    checker = EmailIntelligence()
    return checker.full_scan(email)

# Command line usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_email_check(sys.argv[1])
    else:
        print(Fore.RED + "Usage: python email_check.py email@example.com")