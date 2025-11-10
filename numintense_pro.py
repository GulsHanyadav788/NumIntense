#!/usr/bin/env python3
"""
🔥 NumIntense Pro - Ultimate OSINT Intelligence Suite
Description: Advanced Phone Number Intelligence & Digital Reconnaissance Platform
Version: 4.0.0 | Enhanced Edition
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
import whois
from bs4 import BeautifulSoup

# Initialize colorama
init(autoreset=True)

class NumIntensePro:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (NumIntensePro/4.0.0)'
        })
        self.results = {}
        self.case_id = self.generate_case_id()
        
    def generate_case_id(self):
        """Generate unique case ID for investigation"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        return f"NIP-{timestamp}-{random_id}"

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
        print(Fore.YELLOW + f"    🚀 Version 4.0.0 | Enhanced Edition | Case ID: {self.case_id}")
        print(Fore.GREEN + f"    📅 Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.CYAN + "    " + "═" * 70)
        print()

    def print_status(self, module, message, status="INFO"):
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
            "INFO": "🔹",
            "PROCESSING": "🔄"
        }
        
        color = status_colors.get(status, Fore.WHITE)
        icon = status_icons.get(status, "🔹")
        
        print(f"{color}{icon} [{module}] {message}")

    def validate_number(self, number):
        """Validate and parse phone number"""
        try:
            # Clean the number
            number = re.sub(r'[^\d+]', '', number)
            
            # Add country code if missing
            if not number.startswith('+'):
                self.print_status("VALIDATION", "No country code detected. Assuming +91 (India)", "WARNING")
                number = '+91' + number
            
            parsed = phonenumbers.parse(number)
            if not phonenumbers.is_valid_number(parsed):
                self.print_status("VALIDATION", "Invalid phone number format", "ERROR")
                return None
                
            self.results['raw_number'] = number
            self.results['parsed_number'] = parsed
            self.print_status("VALIDATION", "Phone number validated successfully", "SUCCESS")
            return parsed
            
        except Exception as e:
            self.print_status("VALIDATION", f"Error parsing number: {e}", "ERROR")
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

        # Validation info
        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        
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
            phonenumbers.PhoneNumberType.VOIP: "🌐 VOIP",
            phonenumbers.PhoneNumberType.UNKNOWN: "❓ Unknown"
        }
        number_type_str = type_map.get(number_type, "❓ Unknown")
        print(f"    🔧 {Fore.WHITE}Number Type: {Fore.CYAN}{number_type_str}")

    def check_spam_databases(self, number):
        """Check multiple spam databases for reputation"""
        self.print_status("SPAM", "Checking spam reputation databases...", "PROCESSING")
        
        clean_num = number.replace('+', '')
        spam_results = []
        
        # Check Tellows
        try:
            response = self.session.get(f"https://www.tellows.com/num/{clean_num}", timeout=10)
            if "score" in response.text.lower():
                spam_results.append(("Tellows", "Data Available"))
            else:
                spam_results.append(("Tellows", "No Data"))
        except:
            spam_results.append(("Tellows", "Connection Failed"))
        
        # Display results
        print(f"\n    🚫 {Fore.WHITE}Spam Database Results:")
        for db, status in spam_results:
            if "Available" in status:
                print(f"       {Fore.GREEN}✅ {db}: {status}")
            elif "No Data" in status:
                print(f"       {Fore.YELLOW}⚠️  {db}: {status}")
            else:
                print(f"       {Fore.RED}❌ {db}: {status}")

    def check_social_presence(self, number):
        """Check social media presence"""
        self.print_status("SOCIAL", "Analyzing social media presence...", "PROCESSING")
        
        clean_num = number.replace('+', '').replace(' ', '')
        
        # Check Facebook pattern
        try:
            fb_url = f"https://www.facebook.com/{clean_num}"
            response = self.session.head(fb_url, timeout=5)
            if response.status_code == 200:
                print(f"    📘 {Fore.WHITE}Facebook: {Fore.GREEN}Possible Profile Found")
            else:
                print(f"    📘 {Fore.WHITE}Facebook: {Fore.YELLOW}No Direct Profile")
        except:
            print(f"    📘 {Fore.WHITE}Facebook: {Fore.RED}Check Failed")

        # Check Telegram pattern
        try:
            tg_url = f"https://t.me/{clean_num}"
            response = self.session.head(tg_url, timeout=5)
            if response.status_code == 200:
                print(f"    📱 {Fore.WHITE}Telegram: {Fore.GREEN}Possible Profile Found")
            else:
                print(f"    📱 {Fore.WHITE}Telegram: {Fore.YELLOW}No Direct Profile")
        except:
            print(f"    📱 {Fore.WHITE}Telegram: {Fore.RED}Check Failed")

    def check_breaches(self, email):
        """Check email breaches with actual data"""
        self.print_status("BREACH", f"Checking breaches for: {email}", "PROCESSING")
        
        try:
            # Check HIBP via API (free tier)
            headers = {
                'User-Agent': 'NumIntensePro-Breach-Checker',
                'hibp-api-key': ''  # Add free API key if available
            }
            
            response = self.session.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                breaches = response.json()
                print(f"    🔥 {Fore.WHITE}Breaches Found: {Fore.RED}{len(breaches)}")
                for breach in breaches[:3]:  # Show first 3 breaches
                    print(f"       {Fore.YELLOW}• {breach.get('Name', 'Unknown')} - {breach.get('BreachDate', 'Unknown')}")
            elif response.status_code == 404:
                print(f"    ✅ {Fore.WHITE}Breaches: {Fore.GREEN}No breaches found")
            else:
                print(f"    ℹ️  {Fore.WHITE}Breaches: {Fore.YELLOW}Check manually at hibp.com")
                
        except Exception as e:
            print(f"    ❌ {Fore.WHITE}Breaches: {Fore.RED}Check failed - visit hibp.com")

    def advanced_whois_lookup(self, domain):
        """Enhanced WHOIS lookup with more details"""
        self.print_status("DOMAIN", f"Advanced domain analysis: {domain}", "PROCESSING")
        
        try:
            domain_info = whois.whois(domain)
            
            print(f"    🌐 {Fore.WHITE}Domain: {Fore.GREEN}{domain_info.domain_name}")
            print(f"    🏢 {Fore.WHITE}Registrar: {Fore.CYAN}{domain_info.registrar}")
            
            # Domain age calculation
            if domain_info.creation_date:
                if isinstance(domain_info.creation_date, list):
                    created = domain_info.creation_date[0]
                else:
                    created = domain_info.creation_date
                
                if hasattr(created, 'strftime'):
                    domain_age = (datetime.now() - created).days
                    print(f"    📅 {Fore.WHITE}Age: {Fore.CYAN}{domain_age} days")
            
            # Expiry status
            if domain_info.expiration_date:
                if isinstance(domain_info.expiration_date, list):
                    expires = domain_info.expiration_date[0]
                else:
                    expires = domain_info.expiration_date
                
                if hasattr(expires, 'strftime'):
                    days_left = (expires - datetime.now()).days
                    status_color = Fore.GREEN if days_left > 30 else Fore.RED
                    print(f"    ⏳ {Fore.WHITE}Expires in: {status_color}{days_left} days")
            
            # Name servers
            if domain_info.name_servers:
                print(f"    🔧 {Fore.WHITE}Name Servers: {Fore.CYAN}{len(domain_info.name_servers)} found")
                
        except Exception as e:
            self.print_status("WHOIS", f"Error: {e}", "ERROR")

    def generate_intelligence_report(self, target, target_type):
        """Generate comprehensive intelligence report"""
        print(Fore.CYAN + Style.BRIGHT + "\n    📈 INTELLIGENCE SUMMARY")
        print(Fore.CYAN + "    " + "─" * 50)
        
        if target_type == "phone":
            print(f"    🎯 {Fore.WHITE}Target Type: {Fore.GREEN}Phone Number")
            print(f"    📞 {Fore.WHITE}Number: {Fore.CYAN}{target}")
            print(f"    🔍 {Fore.WHITE}Analysis: {Fore.YELLOW}Basic + Carrier + Social Presence")
            
        elif target_type == "email":
            print(f"    🎯 {Fore.WHITE}Target Type: {Fore.GREEN}Email Address") 
            print(f"    📧 {Fore.WHITE}Email: {Fore.CYAN}{target}")
            print(f"    🔍 {Fore.WHITE}Analysis: {Fore.YELLOW}Breach Check + Domain Analysis")
            
        elif target_type == "domain":
            print(f"    🎯 {Fore.WHITE}Target Type: {Fore.GREEN}Domain")
            print(f"    🌐 {Fore.WHITE}Domain: {Fore.CYAN}{target}")
            print(f"    🔍 {Fore.WHITE}Analysis: {Fore.YELLOW}WHOIS + Registration Details")
        
        print(f"    ⚡ {Fore.WHITE}Status: {Fore.GREEN}Analysis Complete")
        print(f"    📋 {Fore.WHITE}Report ID: {Fore.CYAN}{self.case_id}")

    def run_advanced_scan(self, target, target_type):
        """Run advanced intelligence scan"""
        self.print_status("SCAN", f"Starting advanced {target_type} analysis...", "PROCESSING")
        
        if target_type == "phone":
            parsed = self.validate_number(target)
            if parsed:
                self.get_basic_info(parsed)
                self.check_spam_databases(target)
                self.check_social_presence(target)
                
        elif target_type == "email":
            self.check_breaches(target)
            # Extract domain from email for additional analysis
            domain = target.split('@')[-1]
            self.advanced_whois_lookup(domain)
            
        elif target_type == "domain":
            self.advanced_whois_lookup(target)
        
        self.generate_intelligence_report(target, target_type)

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
    required_modules = ['phonenumbers', 'colorama', 'requests', 'whois', 'bs4']
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
{Fore.WHITE}  {sys.argv[0]} +919876543210 --advanced    {Fore.YELLOW}# Advanced investigation  
{Fore.WHITE}  {sys.argv[0]} admin@company.com --email   {Fore.YELLOW}# Email forensics
{Fore.WHITE}  {sys.argv[0]} target.com --domain         {Fore.YELLOW}# Domain intelligence

{Fore.MAGENTA}Enhanced Features:
{Fore.CYAN}  --advanced   {Fore.WHITE}Advanced intelligence with actual data
{Fore.CYAN}  --quiet      {Fore.WHITE}Minimal output for automated operations
{Fore.CYAN}  --email      {Fore.WHITE}Target is an email address
{Fore.CYAN}  --domain     {Fore.WHITE}Target is a domain
        """
    )
    
    parser.add_argument("target", help="Target (phone number, email, or domain)")
    parser.add_argument("-a", "--advanced", action="store_true", help="Run advanced intelligence gathering")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress banner and minimize output")
    parser.add_argument("--email", action="store_true", help="Target is an email address")
    parser.add_argument("--domain", action="store_true", help="Target is a domain")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    # Initialize tool
    tool = NumIntensePro()
    
    # Display banner
    if not args.quiet:
        tool.print_banner()
    
    # Determine target type and execute appropriate checks
    try:
        if args.email:
            target_type = "email"
            if args.advanced:
                tool.run_advanced_scan(args.target, target_type)
            else:
                tool.print_status("EMAIL", f"Basic email check: {args.target}", "INFO")
                tool.check_breaches(args.target)
                
        elif args.domain:
            target_type = "domain" 
            if args.advanced:
                tool.run_advanced_scan(args.target, target_type)
            else:
                tool.print_status("DOMAIN", f"Basic domain check: {args.target}", "INFO")
                tool.advanced_whois_lookup(args.target)
                
        else:
            target_type = "phone"
            if args.advanced:
                tool.run_advanced_scan(args.target, target_type)
            else:
                tool.print_status("PHONE", f"Basic phone check: {args.target}", "INFO")
                parsed = tool.validate_number(args.target)
                if parsed:
                    tool.get_basic_info(parsed)

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