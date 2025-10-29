#!/usr/bin/env python3

"""
🔥 NumIntense Pro - Ultimate OSINT Intelligence Suite
Description: Advanced Phone Number Intelligence & Digital Reconnaissance Platform
Version: 3.0.0 | Enterprise Edition
Author: GulsHan Kumar & Security Research Team
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
from colorama import init, Fore, Style, Back
import re
import random

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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (NumIntensePro/3.0)'
        })
        self.results = {}
        self.config = self.load_config(config_file)
        self.case_id = self.generate_case_id()
        
        # Initialize modules
        if MODULES_AVAILABLE:
            self.email_checker = EmailBreachChecker()
            self.facebook_osint = AdvancedFacebookOSINT()
            self.dork_generator = AdvancedDorkGenerator()
            self.spam_checker = AdvancedSpamChecker()
            self.telegram_lookup = AdvancedTelegramLookup()
            self.truecaller_lookup = AdvancedTruecallerLookup()
            self.whois_lookup = AdvancedWHOISLookup()

    def generate_case_id(self):
        """Generate unique case ID for investigation"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        return f"NIP-{timestamp}-{random_id}"

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
                "save_reports": False,
                "stealth_mode": False
            }
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                self.print_status("CONFIG", f"Configuration loaded from {config_file}", "SUCCESS")
            else:
                self.print_status("CONFIG", "Config file not found. Using defaults.", "WARNING")
                self.create_sample_config(config_file)
                
        except Exception as e:
            self.print_status("CONFIG", f"Error loading config: {e}", "ERROR")
            
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
                "save_reports": False,
                "stealth_mode": False
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(sample_config, f, indent=4)
            self.print_status("CONFIG", f"Sample config created: {config_file}", "INFO")
        except Exception as e:
            self.print_status("CONFIG", f"Error creating sample config: {e}", "ERROR")

    def print_status(self, module, message, status):
        """Print formatted status messages"""
        status_colors = {
            "SUCCESS": Fore.GREEN,
            "ERROR": Fore.RED,
            "WARNING": Fore.YELLOW,
            "INFO": Fore.CYAN,
            "PROCESSING": Fore.BLUE
        }
        
        status_icons = {
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️",
            "INFO": "ℹ️",
            "PROCESSING": "🔄"
        }
        
        color = status_colors.get(status, Fore.WHITE)
        icon = status_icons.get(status, "🔹")
        
        print(f"{color}{icon} [{module}] {message}")

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
        print(Fore.YELLOW + f"    🚀 Version 3.0.0 | Enterprise Edition | Case ID: {self.case_id}")
        print(Fore.GREEN + f"    📅 Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(Fore.CYAN + "    " + "═" * 70)
        print()

    def validate_number(self, number):
        """Validate and parse phone number"""
        try:
            # Clean the number
            number = re.sub(r'[^\d+]', '', number)
            
            # Add country code if missing
            if not number.startswith('+'):
                self.print_status("VALIDATION", "No country code detected. Assuming +1 (US/Canada)", "WARNING")
                number = '+1' + number
            
            parsed = phonenumbers.parse(number)
            if not phonenumbers.is_valid_number(parsed):
                self.print_status("VALIDATION", "Invalid phone number format", "ERROR")
                return None
                
            self.results['raw_number'] = number
            self.results['parsed_number'] = parsed
            self.print_status("VALIDATION", "Phone number validated successfully", "SUCCESS")
            return parsed
            
        except phonenumbers.NumberParseException as e:
            self.print_status("VALIDATION", f"Error parsing number: {e}", "ERROR")
            return None
        except Exception as e:
            self.print_status("VALIDATION", f"Unexpected error during validation: {e}", "ERROR")
            return None

    def get_basic_info(self, parsed):
        """Display comprehensive basic information"""
        print(Fore.CYAN + Style.BRIGHT + "\n    📊 BASIC INTELLIGENCE REPORT")
        print(Fore.CYAN + "    " + "─" * 50)
        
        # Phone number formats
        international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        
        print(f"    📱 {Fore.WHITE}Number: {Fore.GREEN}{international}")
        print(f"    🔢 {Fore.WHITE}E164 Format: {Fore.YELLOW}{e164}")
        print(f"    🏠 {Fore.WHITE}National Format: {Fore.YELLOW}{national}")
        
        # Location information
        country = geocoder.description_for_number(parsed, 'en')
        carrier_name = carrier.name_for_number(parsed, 'en')
        timezones = timezone.time_zones_for_number(parsed)
        region_code = phonenumbers.region_code_for_number(parsed)
        
        print(f"    🌍 {Fore.WHITE}Country: {Fore.CYAN}{country} ({region_code})")
        print(f"    🏢 {Fore.WHITE}Carrier: {Fore.CYAN}{carrier_name}")
        
        if timezones:
            print(f"    🕐 {Fore.WHITE}Timezone(s): {Fore.CYAN}{', '.join(timezones)}")
        else:
            print(f"    🕐 {Fore.WHITE}Timezone: {Fore.YELLOW}Unknown")
        
        # Validation info
        is_possible = phonenumbers.is_possible_number(parsed)
        is_valid = phonenumbers.is_valid_number(parsed)
        
        valid_status = "✅ Valid" if is_valid else "❌ Invalid"
        possible_status = "✅ Possible" if is_possible else "❌ Not Possible"
        
        print(f"    ✅ {Fore.WHITE}Validation: {Fore.GREEN if is_valid else Fore.RED}{valid_status}")
        print(f"    🔍 {Fore.WHITE}Possibility: {Fore.GREEN if is_possible else Fore.RED}{possible_status}")
        
        # Number type with emoji
        number_type = phonenumbers.number_type(parsed)
        type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "📱 Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "🏠 Fixed Line",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "📞 Fixed Line or Mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "🆓 Toll Free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "💎 Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "💰 Shared Cost",
            phonenumbers.PhoneNumberType.VOIP: "🌐 VOIP",
            phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "👤 Personal Number",
            phonenumbers.PhoneNumberType.PAGER: "📟 Pager",
            phonenumbers.PhoneNumberType.UAN: "🏢 UAN",
            phonenumbers.PhoneNumberType.VOICEMAIL: "📩 Voicemail",
            phonenumbers.PhoneNumberType.UNKNOWN: "❓ Unknown"
        }
        number_type_str = type_map.get(number_type, "❓ Unknown")
        print(f"    🔧 {Fore.WHITE}Number Type: {Fore.CYAN}{number_type_str}")

    def run_api_checks(self, number):
        """Run all available API checks"""
        if not APIS_AVAILABLE:
            self.print_status("API", "API modules not available", "WARNING")
            return
            
        self.print_status("INTELLIGENCE", "Starting API-based intelligence gathering...", "PROCESSING")
        
        # NumVerify API Check
        if self.config['apis']['numverify']:
            try:
                self.print_status("NUMVERIFY", "Querying NumVerify API...", "PROCESSING")
                api = NumVerifyAPI(self.config['apis']['numverify'])
                result = api.validate_number(number)
                
                if result['valid']:
                    self.print_status("NUMVERIFY", "Valid number detected", "SUCCESS")
                    print(f"    🌍 Location: {result.get('location', 'N/A')}")
                    print(f"    🏢 Line Type: {result.get('line_type', 'N/A')}")
                else:
                    self.print_status("NUMVERIFY", result.get('error', 'API error'), "WARNING")
                    
            except Exception as e:
                self.print_status("NUMVERIFY", f"API Error: {e}", "ERROR")
            
            time.sleep(self.config['settings']['rate_limit_delay'])

    def run_osint_checks(self, number):
        """Run all OSINT checks"""
        if not MODULES_AVAILABLE:
            self.print_status("OSINT", "OSINT modules not available", "ERROR")
            return
            
        save_reports = self.config['settings']['save_reports']
        
        # Intelligence Modules
        modules = [
            ("🚫 SPAM ANALYSIS", self.spam_checker.spam_check, [number, save_reports]),
            ("📱 TELEGRAM INTEL", self.telegram_lookup.telegram_lookup, [number, save_reports]),
            ("📞 TRUECALLER ENGINE", self.truecaller_lookup.truecaller_lookup, [number, save_reports]),
            ("👤 FACEBOOK OSINT", self.facebook_osint.facebook_check, [number, save_reports]),
            ("🎯 DORK GENERATION", self.dork_generator.generate_dorks, [number, save_reports])
        ]
        
        for module_name, module_func, args in modules:
            self.print_status("INTELLIGENCE", f"Running {module_name}...", "PROCESSING")
            try:
                module_func(*args)
                time.sleep(1)  # Rate limiting between modules
            except Exception as e:
                self.print_status(module_name.split()[1], f"Module error: {e}", "ERROR")

    def run_email_checks(self, email):
        """Run email breach checks"""
        if not MODULES_AVAILABLE:
            self.print_status("EMAIL", "Email module not available", "ERROR")
            return
            
        self.print_status("EMAIL", f"Starting email forensics for: {email}", "PROCESSING")
        self.email_checker.email_breach_check(email)

    def run_whois_lookup(self, domain):
        """Run WHOIS lookup"""
        if not MODULES_AVAILABLE:
            self.print_status("WHOIS", "WHOIS module not available", "ERROR")
            return
            
        self.print_status("DOMAIN", f"Starting domain intelligence for: {domain}", "PROCESSING")
        self.whois_lookup.whois_lookup(domain, save_report=self.config['settings']['save_reports'])

    def print_summary(self, target_type):
        """Print investigation summary"""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}    🎯 INVESTIGATION SUMMARY")
        print(Fore.GREEN + "    " + "─" * 50)
        print(f"    📋 {Fore.WHITE}Case ID: {Fore.CYAN}{self.case_id}")
        print(f"    🎯 {Fore.WHITE}Target Type: {Fore.CYAN}{target_type}")
        print(f"    ⏱️  {Fore.WHITE}Duration: {Fore.CYAN}{datetime.now().strftime('%H:%M:%S UTC')}")
        print(f"    📊 {Fore.WHITE}Modules Executed: {Fore.CYAN}{'All' if MODULES_AVAILABLE else 'Basic'}")
        
        if self.config['settings']['save_reports']:
            print(f"    💾 {Fore.WHITE}Reports Saved: {Fore.GREEN}Yes")
        else:
            print(f"    💾 {Fore.WHITE}Reports Saved: {Fore.YELLOW}No")

    def print_legal_notice(self):
        """Print legal disclaimer"""
        print(f"\n{Fore.RED}{Style.BRIGHT}    ⚠️  LEGAL & COMPLIANCE NOTICE")
        print(Fore.RED + "    " + "─" * 50)
        print(f"    {Fore.YELLOW}🔒 This tool is for authorized security research only.")
        print(f"    {Fore.YELLOW}📜 Users must comply with all applicable laws and regulations.")
        print(f"    {Fore.YELLOW}🛡️  Respect privacy and obtain proper authorization.")
        print(f"    {Fore.YELLOW}⚖️  Developers assume no liability for misuse.")

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
        print(Fore.RED + f"❌ Missing required modules: {', '.join(missing_modules)}")
        print(Fore.YELLOW + f"💡 Install with: pip install {' '.join(missing_modules)}")
        return False
    
    print(Fore.GREEN + "✅ All core dependencies verified")
    return True

def main():
    """Main function"""
    if not check_dependencies():
        sys.exit(1)
        
    parser = argparse.ArgumentParser(
        description="🔥 NumIntense Pro - Ultimate OSINT Intelligence Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.CYAN}Examples:
{Fore.WHITE}  {sys.argv[0]} +919876543210               {Fore.YELLOW}# Basic phone intelligence
{Fore.WHITE}  {sys.argv[0]} +919876543210 --full-scan    {Fore.YELLOW}# Comprehensive investigation  
{Fore.WHITE}  {sys.argv[0]} admin@company.com --email    {Fore.YELLOW}# Email forensics
{Fore.WHITE}  {sys.argv[0]} target.com --domain         {Fore.YELLOW}# Domain intelligence
{Fore.WHITE}  {sys.argv[0]} +919876543210 --save         {Fore.YELLOW}# Save reports to files

{Fore.MAGENTA}Enterprise Features:
{Fore.CYAN}  --full-scan    {Fore.WHITE}Comprehensive intelligence gathering
{Fore.CYAN}  --save         {Fore.WHITE}Generate professional reports
{Fore.CYAN}  --stealth      {Fore.WHITE}Enable stealth mode operations
{Fore.CYAN}  --quiet        {Fore.WHITE}Minimal output for automated operations
        """
    )
    
    parser.add_argument("target", help="Target (phone number, email, or domain)")
    parser.add_argument("-f", "--full-scan", action="store_true", help="Run comprehensive intelligence gathering")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress banner and minimize output")
    parser.add_argument("-s", "--save", action="store_true", help="Save intelligence reports to files")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode operations")
    parser.add_argument("-c", "--config", default="config.json", help="Configuration file path")
    parser.add_argument("--email", action="store_true", help="Target is an email address")
    parser.add_argument("--domain", action="store_true", help="Target is a domain")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    # Initialize tool
    tool = NumIntensePro(args.config)
    
    # Update config based on arguments
    if args.save:
        tool.config['settings']['save_reports'] = True
    if args.stealth:
        tool.config['settings']['stealth_mode'] = True
        tool.print_status("STEALTH", "Stealth mode activated", "INFO")
    
    # Display banner
    if not args.quiet:
        tool.print_banner()
    
    # Determine target type and execute appropriate checks
    try:
        if args.email:
            tool.print_status("INVESTIGATION", f"Starting email forensics: {args.target}", "PROCESSING")
            tool.run_email_checks(args.target)
            target_type = "Email Address"
            
        elif args.domain:
            tool.print_status("INVESTIGATION", f"Starting domain intelligence: {args.target}", "PROCESSING")
            tool.run_whois_lookup(args.target)
            target_type = "Domain"
            
        else:
            tool.print_status("INVESTIGATION", f"Starting phone intelligence: {args.target}", "PROCESSING")
            parsed = tool.validate_number(args.target)
            if parsed:
                tool.get_basic_info(parsed)
                
                if args.full_scan:
                    tool.print_status("INTELLIGENCE", "Initiating full spectrum analysis...", "PROCESSING")
                    tool.run_api_checks(args.target)
                    tool.run_osint_checks(args.target)
                else:
                    tool.print_status("INTELLIGENCE", "Running standard OSINT checks...", "PROCESSING")
                    tool.run_osint_checks(args.target)
                
                target_type = "Phone Number"
            else:
                sys.exit(1)
        
        # Print summary
        tool.print_summary(target_type)
        
        # Legal notice
        if not args.quiet:
            tool.print_legal_notice()
            
        print(f"\n{Fore.GREEN}{Style.BRIGHT}    🎉 Investigation completed successfully!")
        print(f"    📁 Case ID: {tool.case_id}")
        
    except KeyboardInterrupt:
        tool.print_status("SYSTEM", "Investigation interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        tool.print_status("SYSTEM", f"Unexpected error: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()