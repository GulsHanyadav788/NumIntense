#!/usr/bin/env python3
"""
🔥 NumIntense - Advanced OSINT & Phone Number Intelligence Tool
Description: Ultimate Digital Reconnaissance Platform
Version: 3.1.0 | Stable Edition
Author: GulsHan Kumar
License: MIT
"""

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import argparse
import sys
import requests
import json
import time
import os
from datetime import datetime
from colorama import init, Fore, Style
import re
import random

# Initialize colorama
init(autoreset=True)

class NumIntense:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (NumIntense/3.1.0)'
        })
        self.results = {}
        self.case_id = self.generate_case_id()
        
    def generate_case_id(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        return f"NI-{timestamp}-{random_id}"

    def print_banner(self):
        """Display professional banner"""
        print(Fore.MAGENTA + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    ███╗   ██╗██╗   ██╗███╗   ███╗██╗███╗   ██╗████████╗███████╗███╗   ██╗███████╗    ║
    ║    ████╗  ██║██║   ██║████╗ ████║██║████╗  ██║╚══██╔══╝██╔════╝████╗  ██║██╔════╝    ║
    ║    ██╔██╗ ██║██║   ██║██╔████╔██║██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║█████╗      ║
    ║    ██║╚██╗██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║██╔══╝      ║
    ║    ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║   ██║   ███████╗██║ ╚████║███████╗    ║
    ║    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝    ║
    ║                                                                              ║
    ║                    🔥 ULTIMATE OSINT INTELLIGENCE SUITE                     ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        print(Fore.CYAN + Style.BRIGHT + "    " + "═" * 70)
        print(Fore.YELLOW + f"    🚀 Version 3.1.0 | Enterprise Edition | Case ID: {self.case_id}")
        print(Fore.GREEN + f"    📅 Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(Fore.CYAN + "    " + "═" * 70)
        print()

    def print_status(self, module, message, status="INFO"):
        status_config = {
            "SUCCESS": {"color": Fore.GREEN, "icon": "✅"},
            "ERROR": {"color": Fore.RED, "icon": "❌"},
            "WARNING": {"color": Fore.YELLOW, "icon": "⚠️"},
            "INFO": {"color": Fore.CYAN, "icon": "🔹"},
            "PROCESSING": {"color": Fore.BLUE, "icon": "🔄"}
        }
        
        config = status_config.get(status, status_config["INFO"])
        print(f"{config['color']}{config['icon']} [{module}] {message}")

    def validate_number(self, number):
        try:
            number = re.sub(r'[^\d+]', '', number)
            
            if not number.startswith('+'):
                self.print_status("VALIDATION", "No country code. Assuming +91 (India)", "WARNING")
                number = '+91' + number
            
            parsed = phonenumbers.parse(number)
            if not phonenumbers.is_valid_number(parsed):
                self.print_status("VALIDATION", "Invalid phone number", "ERROR")
                return None
                
            self.results['raw_number'] = number
            self.results['parsed_number'] = parsed
            self.print_status("VALIDATION", "Number validated", "SUCCESS")
            return parsed
            
        except Exception as e:
            self.print_status("VALIDATION", f"Error: {e}", "ERROR")
            return None

    def get_basic_info(self, parsed):
        print(Fore.CYAN + Style.BRIGHT + "\n    📊 BASIC INFORMATION")
        print(Fore.CYAN + "    " + "─" * 40)
        
        international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        
        print(f"    📱 {Fore.WHITE}Number: {Fore.GREEN}{international}")
        print(f"    🔢 {Fore.WHITE}E164: {Fore.YELLOW}{e164}")
        print(f"    🏠 {Fore.WHITE}National: {Fore.YELLOW}{national}")
        
        country = geocoder.description_for_number(parsed, 'en')
        carrier_name = carrier.name_for_number(parsed, 'en')
        timezones = timezone.time_zones_for_number(parsed)
        region_code = phonenumbers.region_code_for_number(parsed)
        
        print(f"    🌍 {Fore.WHITE}Country: {Fore.CYAN}{country} ({region_code})")
        print(f"    🏢 {Fore.WHITE}Carrier: {Fore.CYAN}{carrier_name}")
        
        if timezones:
            print(f"    🕐 {Fore.WHITE}Timezone: {Fore.CYAN}{', '.join(timezones)}")

        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        
        valid_status = "✅ Valid" if is_valid else "❌ Invalid"
        possible_status = "✅ Possible" if is_possible else "❌ Not Possible"
        
        print(f"    ✅ {Fore.WHITE}Validation: {Fore.GREEN if is_valid else Fore.RED}{valid_status}")
        print(f"    🔍 {Fore.WHITE}Possibility: {Fore.GREEN if is_possible else Fore.RED}{possible_status}")
        
        number_type = phonenumbers.number_type(parsed)
        type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "📱 Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "🏠 Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "📞 Fixed/Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "🆓 Toll Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "💎 Premium",
            phonenumbers.PhoneNumberType.VOIP: "🌐 VOIP",
            phonenumbers.PhoneNumberType.UNKNOWN: "❓ Unknown"
        }
        number_type_str = type_map.get(number_type, "❓ Unknown")
        print(f"    🔧 {Fore.WHITE}Type: {Fore.CYAN}{number_type_str}")

    def run_osint_checks(self, number):
        self.print_status("OSINT", "Starting intelligence gathering...", "PROCESSING")
        
        # Social Media Checks
        self.check_social_media(number)
        
        # Spam Check
        self.check_spam(number)
        
        # Telegram Lookup
        self.check_telegram(number)
        
        # Truecaller Lookup
        self.check_truecaller(number)

    def check_social_media(self, number):
        self.print_status("SOCIAL", "Checking social media platforms...", "PROCESSING")
        
        clean_num = number.replace('+', '').replace(' ', '')
        platforms = {
            "Facebook": f"https://www.facebook.com/search/top/?q={clean_num}",
            "Instagram": f"https://www.instagram.com/search/top/?q={clean_num}",
            "Twitter": f"https://twitter.com/search?q={clean_num}",
            "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={clean_num}",
            "Telegram": f"https://t.me/{clean_num}",
        }
        
        for platform, url in platforms.items():
            print(f"    🔗 {Fore.WHITE}{platform}: {Fore.CYAN}{url}")

    def check_spam(self, number):
        self.print_status("SPAM", "Checking spam databases...", "PROCESSING")
        
        clean_num = number.replace('+', '')
        spam_sites = {
            "Tellows": f"https://www.tellows.com/search?num={clean_num}",
            "ShouldIAnswer": f"https://www.shouldianswer.com/phone-number/{clean_num}",
            "TrueCaller": f"https://www.truecaller.com/search/{clean_num}",
        }
        
        for site, url in spam_sites.items():
            print(f"    🚫 {Fore.WHITE}{site}: {Fore.CYAN}{url}")

    def check_telegram(self, number):
        self.print_status("TELEGRAM", "Generating Telegram links...", "PROCESSING")
        
        clean_num = number.replace('+', '').replace(' ', '')
        variations = [
            clean_num,
            f"user{clean_num}",
            f"id{clean_num}",
            clean_num[-10:],
            f"user{clean_num[-10:]}"
        ]
        
        for username in variations[:3]:
            print(f"    📱 {Fore.WHITE}Telegram: {Fore.CYAN}https://t.me/{username}")

    def check_truecaller(self, number):
        self.print_status("TRUECALLER", "Checking Truecaller...", "PROCESSING")
        
        clean_num = number.replace('+', '').replace(' ', '')
        urls = [
            f"https://www.truecaller.com/search/{clean_num}",
            f"https://www.truecaller.com/search/in/{clean_num}",
        ]
        
        for url in urls:
            print(f"    📞 {Fore.WHITE}Truecaller: {Fore.CYAN}{url}")

    def run_email_check(self, email):
        self.print_status("EMAIL", f"Checking breaches for: {email}", "PROCESSING")
        
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.print_status("EMAIL", "Invalid email format", "ERROR")
            return
        
        print(f"    📧 {Fore.WHITE}Have I Been Pwned: {Fore.CYAN}https://haveibeenpwned.com/account/{email}")
        print(f"    🔍 {Fore.WHITE}Google Dork: {Fore.CYAN}intext:'{email}'")
        print(f"    🌐 {Fore.WHITE}Social Search: {Fore.CYAN}site:facebook.com '{email}'")

    def run_whois_lookup(self, domain):
        self.print_status("WHOIS", f"Looking up domain: {domain}", "PROCESSING")
        
        try:
            import whois
            domain_info = whois.whois(domain)
            
            print(f"    🌐 {Fore.WHITE}Domain: {Fore.GREEN}{domain_info.domain_name}")
            print(f"    🏢 {Fore.WHITE}Registrar: {Fore.CYAN}{domain_info.registrar}")
            print(f"    📅 {Fore.WHITE}Created: {Fore.CYAN}{domain_info.creation_date}")
            print(f"    📅 {Fore.WHITE}Expires: {Fore.CYAN}{domain_info.expiration_date}")
            
            if domain_info.name_servers:
                print(f"    🔧 {Fore.WHITE}Name Servers: {Fore.CYAN}{', '.join(list(domain_info.name_servers)[:2])}")
                
        except Exception as e:
            self.print_status("WHOIS", f"Error: {e}", "ERROR")

    def print_summary(self):
        print(f"\n{Fore.GREEN}{Style.BRIGHT}    🎉 INVESTIGATION COMPLETE!")
        print(Fore.GREEN + "    " + "─" * 40)
        print(f"    📋 {Fore.WHITE}Case ID: {Fore.CYAN}{self.case_id}")
        print(f"    ⏱️  {Fore.WHITE}Completed: {Fore.CYAN}{datetime.now().strftime('%H:%M:%S')}")
        print(f"    📊 {Fore.WHITE}Modules: {Fore.CYAN}Basic + OSINT")

    def print_legal(self):
        print(f"\n{Fore.RED}{Style.BRIGHT}    ⚠️  LEGAL DISCLAIMER")
        print(Fore.RED + "    " + "─" * 40)
        print(f"    {Fore.YELLOW}🔒 For authorized security research only")
        print(f"    {Fore.YELLOW}📜 Comply with all applicable laws")
        print(f"    {Fore.YELLOW}🛡️  Respect privacy and get authorization")

def check_dependencies():
    required = ['phonenumbers', 'colorama', 'requests']
    missing = []
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(Fore.RED + f"❌ Missing: {', '.join(missing)}")
        print(Fore.YELLOW + f"💡 Install: pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    if not check_dependencies():
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="NumIntense - OSINT Intelligence Tool")
    parser.add_argument("target", help="Phone number, email, or domain")
    parser.add_argument("-f", "--full", action="store_true", help="Full OSINT scan")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode")
    parser.add_argument("--email", action="store_true", help="Target is email")
    parser.add_argument("--domain", action="store_true", help="Target is domain")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    tool = NumIntense()
    
    if not args.quiet:
        tool.print_banner()
    
    try:
        if args.email:
            tool.print_status("INVESTIGATION", f"Email analysis: {args.target}", "PROCESSING")
            tool.run_email_check(args.target)
            
        elif args.domain:
            tool.print_status("INVESTIGATION", f"Domain analysis: {args.target}", "PROCESSING")
            tool.run_whois_lookup(args.target)
            
        else:
            tool.print_status("INVESTIGATION", f"Phone analysis: {args.target}", "PROCESSING")
            parsed = tool.validate_number(args.target)
            if parsed:
                tool.get_basic_info(parsed)
                
                if args.full:
                    tool.run_osint_checks(args.target)
                else:
                    tool.print_status("INFO", "Use -f for full OSINT scan", "INFO")
        
        tool.print_summary()
        
        if not args.quiet:
            tool.print_legal()
            
        print(f"\n{Fore.GREEN}✅ Done! Case: {tool.case_id}")
        
    except KeyboardInterrupt:
        tool.print_status("SYSTEM", "Interrupted by user", "WARNING")
    except Exception as e:
        tool.print_status("SYSTEM", f"Error: {e}", "ERROR")

if __name__ == "__main__":
    main()