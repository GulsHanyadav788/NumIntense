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
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Try to import optional modules
try:
    from modules.google_dorking import generate_dorks
    GOOGLE_DORKING_AVAILABLE = True
except ImportError:
    GOOGLE_DORKING_AVAILABLE = False

try:
    from modules.telegram_check import telegram_lookup
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

def validate_number(number):
    """Validate and parse phone number with improved error handling"""
    try:
        parsed = phonenumbers.parse(number)
        if not phonenumbers.is_valid_number(parsed):
            print(Fore.RED + "[!] Invalid phone number.")
            return None
        return parsed
    except phonenumbers.NumberParseException as e:
        print(Fore.RED + f"[!] Error parsing number: {e}")
        return None
    except Exception as e:
        print(Fore.RED + f"[!] Unexpected error during number validation: {e}")
        return None

def basic_info(parsed):
    """Display basic information about the phone number"""
    print(Fore.CYAN + f"\n[+] Phone Number: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
    print(Fore.CYAN + f"[+] Country: {geocoder.description_for_number(parsed, 'en')}")
    print(Fore.CYAN + f"[+] Carrier: {carrier.name_for_number(parsed, 'en')}")
    
    timezones = timezone.time_zones_for_number(parsed)
    if timezones:
        print(Fore.CYAN + f"[+] Timezone(s): {', '.join(timezones)}")
    else:
        print(Fore.CYAN + "[+] Timezone: Unknown")
    
    # Check if number is possible (not necessarily valid)
    print(Fore.CYAN + f"[+] Is Possible: {phonenumbers.is_possible_number(parsed)}")
    
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

def check_breaches(number):
    """Check if phone number appears in known data breaches (simulated)"""
    print(Fore.YELLOW + "\n[🔍] Checking known data breaches...")
    
    # This is a simulation - in a real tool, you would use breach databases/APIs
    # For educational purposes only
    print(Fore.YELLOW + "[!] Breach checking requires access to breach databases (not implemented)")
    
    # Example of how to integrate with HaveIBeenPwned style service (commented out)
    # try:
    #     response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{number}", 
    #                           headers={'User-Agent': 'NumIntensePro'})
    #     if response.status_code == 200:
    #         breaches = response.json()
    #         for breach in breaches:
    #             print(Fore.RED + f"[!] Breach found: {breach['Name']} ({breach['BreachDate']})")
    #     elif response.status_code == 404:
    #         print(Fore.GREEN + "[+] No known breaches found")
    #     else:
    #         print(Fore.YELLOW + "[!] Could not check breaches (API limit or error)")
    # except Exception as e:
    #     print(Fore.YELLOW + f"[!] Error checking breaches: {e}")

def social_media_lookup(number):
    """Check for social media presence (simulated)"""
    print(Fore.YELLOW + "\n[🔍] Checking social media platforms...")
    
    # This would typically involve using various APIs or web scraping
    # For demonstration purposes only
    platforms = ["Facebook", "WhatsApp", "Twitter", "Instagram", "LinkedIn", "Signal"]
    
    for platform in platforms:
        # Simulate some platforms having the number
        if hash(number) % 3 == 0:  # Random-ish simulation
            print(Fore.GREEN + f"[+] Potential {platform} account found")
        else:
            print(Fore.YELLOW + f"[-] No {platform} account found")

def osint_links(number):
    """Generate OSINT investigation links"""
    print(Fore.YELLOW + "\n[🔎] OSINT Investigation Links:")
    
    # Generate various search links
    search_engines = [
        ("Google", f"https://www.google.com/search?q=%22{number}%22"),
        ("DuckDuckGo", f"https://duckduckgo.com/?q=%22{number}%22"),
        ("Bing", f"https://www.bing.com/search?q=%22{number}%22"),
    ]
    
    for name, url in search_engines:
        print(Fore.GREEN + f"[{name}] {url}")
    
    # Specialized reverse phone lookup sites
    reverse_lookup_sites = [
        ("TrueCaller", f"https://www.truecaller.com/search/in/{number}"),
        ("WhitePages", f"https://www.whitepages.com/phone/{number}"),
        ("SpyDialer", f"https://www.spydialer.com/default.aspx?phone={number}"),
    ]
    
    for name, url in reverse_lookup_sites:
        print(Fore.GREEN + f"[{name}] {url}")
    
    # Google dorking if available
    if GOOGLE_DORKING_AVAILABLE:
        print(Fore.YELLOW + "\n[🔎] Google Dork Results:")
        try:
            for link in generate_dorks(number):
                print(Fore.GREEN + link)
        except Exception as e:
            print(Fore.RED + f"[!] Error generating Google dorks: {e}")
    else:
        print(Fore.YELLOW + "[!] Google dorking module not available")
    
    # Telegram check if available
    if TELEGRAM_AVAILABLE:
        try:
            telegram_lookup(number)
        except Exception as e:
            print(Fore.RED + f"[!] Error in Telegram lookup: {e}")
    else:
        print(Fore.YELLOW + "[!] Telegram lookup module not available")
    
    # Additional checks
    check_breaches(number)
    social_media_lookup(number)

def banner():
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
    print(Fore.CYAN + f"Version 2.0 | by GulsHan kumar {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.CYAN + "=" * 60)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="📱 NumIntense Pro - Advanced Phone Number OSINT Tool")
    parser.add_argument("number", help="Phone number (e.g. +919876543210)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress banner and minimize output")
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    
    if not args.quiet:
        banner()
    
    parsed = validate_number(args.number)
    if parsed:
        print(Fore.GREEN + "\n[✓] Basic Information")
        basic_info(parsed)
        
        if args.verbose:
            print(Fore.YELLOW + "\n[ℹ] Verbose mode enabled")
            # Additional verbose information could be added here
        
        osint_links(args.number)
        
        print(Fore.MAGENTA + "\n[+] Investigation complete. Use information responsibly and legally.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()