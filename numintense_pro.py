#!/usr/bin/env python3

File: numintense_pro.py

Description: Advanced Phone Number OSINT tool (Kali Linux & Termux compatible)

import phonenumbers from phonenumbers import geocoder, carrier, timezone import argparse from modules.google_dorking import generate_dorks from modules.telegram_check import telegram_lookup from colorama import init, Fore

init(autoreset=True)

def validate_number(number): try: parsed = phonenumbers.parse(number) if not phonenumbers.is_valid_number(parsed): print(Fore.RED + "[!] Invalid phone number.") return None return parsed except: print(Fore.RED + "[!] Error parsing number.") return None

def basic_info(parsed): print(Fore.CYAN + f"[+] Country: {geocoder.description_for_number(parsed, 'en')}") print(Fore.CYAN + f"[+] Carrier: {carrier.name_for_number(parsed, 'en')}") print(Fore.CYAN + f"[+] Timezone(s): {timezone.time_zones_for_number(parsed)}")

def osint_links(number): print(Fore.YELLOW + "\n[🔎] Google Dork Results:") for link in generate_dorks(number): print(Fore.GREEN + link) telegram_lookup(number)

def banner(): print(Fore.MAGENTA + """ ███╗   ██╗██╗   ██╗███╗   ███╗██╗███╗   ██╗████████╗███████╗███╗   ██╗███████╗ ████╗  ██║██║   ██║████╗ ████║██║████╗  ██║╚══██╔══╝██╔════╝████╗  ██║██╔════╝ ██╔██╗ ██║██║   ██║██╔████╔██║██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║█████╗
██║╚██╗██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║██╔══╝
██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║   ██║   ███████╗██║ ╚████║███████╗ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝ NumIntense Pro - Phone OSINT Framework """)

def main(): parser = argparse.ArgumentParser(description="📱 NumIntense Pro - Advanced Phone Number OSINT Tool") parser.add_argument("number", help="Phone number (e.g. +919876543210)") args = parser.parse_args()

banner()
parsed = validate_number(args.number)
if parsed:
    print(Fore.GREEN + "\n[✓] Basic Information")
    basic_info(parsed)
    osint_links(args.number)

if name == "main": main()

