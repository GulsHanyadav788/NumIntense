#!/usr/bin/env python3

"""
NumIntense Pro - Advanced Phone Number OSINT Tool
Description: Enhanced phone number intelligence tool with multiple lookup sources
Compatible with Kali Linux, Termux, and other platforms
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

# Import modules
try:
    from modules.email_breach_check import EmailBreachChecker
    from modules.facebook_check import AdvancedFacebookOSINT
    from modules.generate_dorks import AdvancedDorkGenerator
    from modules.spam_check import AdvancedSpamChecker
    from modules.telegram_lookup import AdvancedTelegramLookup
    from modules.truecaller_lookup import AdvancedTruecallerLookup
    from modules.whois_lookup import AdvancedWHOISLookup
    
    MODULES_AVAILABLE = True
except ImportError as e:
    print(Fore.RED + f"[!] Some modules not available: {e}")
    MODULES_AVAILABLE = False

# Import API modules
try:
    from apis.numverify import NumVerifyAPI
    from apis.abstractapi import AbstractAPI
    APIS_AVAILABLE = True
except ImportError:
    APIS_AVAILABLE = False

# Initialize colorama
init(autoreset=True)

class NumIntensePro:
    def __init__(self, config_file="config.json"):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {}
        self.config = self.load_config(config_file)
        
        # Initialize modules
        if MODULES_AVAILABLE:
            self.email_checker = EmailBreachChecker()
            self.facebook_osint = AdvancedFacebookOSINT()
            self.dork_generator = AdvancedDorkGenerator()
            self.spam_checker = AdvancedSpamChecker()
            self.telegram_lookup = AdvancedTelegramLookup()
            self.truecaller_lookup = AdvancedTruecallerLookup()
            self.whois_lookup = AdvancedWHOISLookup()
        
    def load_config(self, config_file):
        """Load API configuration from file"""
        default_config = {
            "apis": {
                "numverify": "",
                "abstractapi": "",
                "hibp": ""
            },
            "settings": {
                "rate_limit_delay": 1,
                "timeout": 10,
                "save_reports": False
            }
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge with default config
                    default_config.update(user_config)
                print(Fore.GREEN + f"[+] Loaded configuration from {config_file}")
            else:
                print(Fore.YELLOW + f"[!] Config file {config_file} not found. Using defaults.")
                self.create_sample_config(config_file)
                
        except Exception as e:
            print(Fore.RED + f"[!] Error loading config: {e}")
            
        return default_config
    
    def create_sample_config(self, config_file):
        """Create sample configuration file"""
        sample_config = {
            "apis": {
                "numverify": "YOUR_NUMVERIFY_API_KEY_HERE",
                "abstractapi": "YOUR_ABSTRACTAPI_KEY_HERE",
                "hibp": "YOUR_HIBP_API_KEY_HERE"
            },
            "settings": {
                "rate_limit_delay": 1,
                "timeout": 10,
                "save_reports": False
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(sample_config, f, indent=4)
            print(Fore.YELLOW + f"[!] Sample config created: {config_file}")
            print(Fore.YELLOW + "[!] Please add your API keys to the config file")
        except Exception as e:
            print(Fore.RED + f"[!] Error creating sample config: {e}")

    def validate_number(self, number):
        """Validate and parse phone number"""
        try:
            # Clean the number
            number = re.sub(r'[^\d+]', '', number)
            
            # Add country code if missing
            if not number.startswith('+'):
                print(Fore.YELLOW + "[!] No country code detected. Assuming +1 (US/Canada)")
                number = '+1' + number
            
            parsed = phonenumbers.parse(number)
            if not phonenumbers.is_valid_number(parsed):
                print(Fore.RED + "[!] Invalid phone number.")
                return None
                
            self.results['raw_number'] = number
            self.results['parsed_number'] = parsed
            return parsed
            
        except phonenumbers.NumberParseException as e:
            print(Fore.RED + f"[!] Error parsing number: {e}")
            return None
        except Exception as e:
            print(Fore.RED + f"[!] Unexpected error during number validation: {e}")
            return None

    def get_basic_info(self, parsed):
        """Display comprehensive basic information"""
        print(Fore.CYAN + f"\n[+] Phone Number: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(Fore.CYAN + f"[+] E164 Format: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
        print(Fore.CYAN + f"[+] National Format: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}")
        
        country = geocoder.description_for_number(parsed, 'en')
        print(Fore.CYAN + f"[+] Country: {country}")
        
        carrier_name = carrier.name_for_number(parsed, 'en')
        print(Fore.CYAN + f"[+] Carrier: {carrier_name}")
        
        timezones = timezone.time_zones_for_number(parsed)
        if timezones:
            print(Fore.CYAN + f"[+] Timezone(s): {', '.join(timezones)}")
        else:
            print(Fore.CYAN + "[+] Timezone: Unknown")
        
        print(Fore.CYAN + f"[+] Is Possible: {phonenumbers.is_possible_number(parsed)}")
        print(Fore.CYAN + f"[+] Is Valid: {phonenumbers.is_valid_number(parsed)}")
        
        # Number type
        number_type = phonenumbers.number_type(parsed)
        type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
            phonenumbers.PhoneNumberType.VOIP: "VOIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
            phonenumbers.PhoneNumberType.UAN: "UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown"
        }
        print(Fore.CYAN + f"[+] Number Type: {type_map.get(number_type, 'Unknown')}")
        
        region_code = phonenumbers.region_code_for_number(parsed)
        print(Fore.CYAN + f"[+] Region Code: {region_code}")

    def run_api_checks(self, number):
        """Run all available API checks"""
        if not APIS_AVAILABLE:
            print(Fore.YELLOW + "[!] API modules not available")
            return
            
        print(Fore.YELLOW + "\n[🔍] Starting API Checks...")
        
        # NumVerify API Check
        if self.config['apis']['numverify']:
            try:
                print(Fore.YELLOW + "[+] Checking NumVerify API...")
                api = NumVerifyAPI(self.config['apis']['numverify'])
                result = api.validate_number(number)
                
                if result['valid']:
                    print(Fore.GREEN + f"[✓] NumVerify - Valid: {result['number']}")
                    print(Fore.GREEN + f"[✓] NumVerify - Country: {result['country']}")
                    print(Fore.GREEN + f"[✓] NumVerify - Carrier: {result['carrier']}")
                else:
                    print(Fore.RED + f"[!] NumVerify: {result['error']}")
                    
            except Exception as e:
                print(Fore.RED + f"[!] NumVerify API Error: {e}")
            
            time.sleep(self.config['settings']['rate_limit_delay'])

    def run_osint_checks(self, number):
        """Run all OSINT checks"""
        if not MODULES_AVAILABLE:
            print(Fore.YELLOW + "[!] OSINT modules not available")
            return
            
        save_reports = self.config['settings']['save_reports']
        
        # Spam Check
        print(Fore.YELLOW + "\n[🚫] Running Spam Check...")
        self.spam_checker.spam_check(number, save_report=save_reports)
        
        # Telegram Lookup
        print(Fore.YELLOW + "\n[📱] Running Telegram Lookup...")
        self.telegram_lookup.telegram_lookup(number, save_report=save_reports)
        
        # Truecaller Lookup
        print(Fore.YELLOW + "\n[📞] Running Truecaller Lookup...")
        self.truecaller_lookup.truecaller_lookup(number, save_report=save_reports)
        
        # Facebook OSINT
        print(Fore.YELLOW + "\n[👤] Running Facebook OSINT...")
        self.facebook_osint.facebook_check(number, save_output=save_reports)
        
        # Dork Generation
        print(Fore.YELLOW + "\n[🎯] Generating Search Dorks...")
        self.dork_generator.generate_dorks(number, save_output=save_reports)

    def run_email_checks(self, email):
        """Run email breach checks"""
        if not MODULES_AVAILABLE:
            print(Fore.YELLOW + "[!] Email module not available")
            return
            
        print(Fore.YELLOW + f"\n[📧] Running Email Breach Check for: {email}")
        self.email_checker.email_breach_check(email)

    def run_whois_lookup(self, domain):
        """Run WHOIS lookup"""
        if not MODULES_AVAILABLE:
            print(Fore.YELLOW + "[!] WHOIS module not available")
            return
            
        print(Fore.YELLOW + f"\n[🌐] Running WHOIS Lookup for: {domain}")
        self.whois_lookup.whois_lookup(domain, save_report=self.config['settings']['save_reports'])

    def banner(self):
        """Display tool banner"""
        print(Fore.MAGENTA + Style.BRIGHT + """
 ███╗   ██╗██╗   ██╗███╗   ███╗██╗███╗   ██╗████████╗███████╗███╗   ██╗███████╗███████╗
 ████╗  ██║██║   ██║████╗ ████║██║████╗  ██║╚══██╔══╝██╔════╝████╗  ██║██╔════╝██╔════╝
 ██╔██╗ ██║██║   ██║██╔████╔██║██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║█████╗  ███████╗
 ██║╚██╗██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║
 ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║   ██║   ███████╗██║ ╚████║███████╗███████║
 ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝
    """)
        print(Fore.CYAN + "NumIntense Pro - Advanced Phone Number OSINT Framework")
        print(Fore.CYAN + f"Version 3.0 | Complete Edition | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.CYAN + "=" * 70)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_modules = ['phonenumbers', 'colorama', 'requests']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(Fore.RED + f"[!] Missing required modules: {', '.join(missing_modules)}")
        print(Fore.YELLOW + "[!] Install them using: pip install " + " ".join(missing_modules))
        return False
    return True

def main():
    """Main function"""
    if not check_dependencies():
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="📱 NumIntense Pro - Advanced Phone Number OSINT Tool")
    parser.add_argument("target", help="Phone number (e.g. +919876543210), email, or domain")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress banner and minimize output")
    parser.add_argument("-a", "--all", action="store_true", help="Run all available checks")
    parser.add_argument("-s", "--save", action="store_true", help="Save results to files")
    parser.add_argument("-c", "--config", default="config.json", help="Config file path")
    parser.add_argument("--email", action="store_true", help="Target is an email address")
    parser.add_argument("--domain", action="store_true", help="Target is a domain")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    
    tool = NumIntensePro(args.config)
    
    # Update config if save flag is set
    if args.save:
        tool.config['settings']['save_reports'] = True
    
    if not args.quiet:
        tool.banner()
    
    # Determine target type
    if args.email:
        # Email check
        tool.run_email_checks(args.target)
        
    elif args.domain:
        # Domain WHOIS check
        tool.run_whois_lookup(args.target)
        
    else:
        # Phone number check
        parsed = tool.validate_number(args.target)
        if parsed:
            print(Fore.GREEN + "\n[✓] Basic Information")
            tool.get_basic_info(parsed)
            
            if args.verbose or args.all:
                print(Fore.YELLOW + "\n[ℹ] Running extended checks...")
                tool.run_api_checks(args.target)
                tool.run_osint_checks(args.target)
            else:
                # Run basic OSINT checks only
                tool.run_osint_checks(args.target)
            
            print(Fore.MAGENTA + "\n" + "="*70)
            print(Fore.MAGENTA + "[+] Investigation complete. Use information responsibly.")
            print(Fore.MAGENTA + "[!] LEGAL DISCLAIMER: For educational and security research only.")
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()