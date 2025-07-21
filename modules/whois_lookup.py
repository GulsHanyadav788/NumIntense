# modules/whois_lookup.py

import whois
from colorama import Fore

def whois_lookup(domain):
    print(Fore.BLUE + f"\n[🌐] WHOIS Lookup for: {domain}")
    try:
        result = whois.whois(domain)
        if result.domain_name:
            print(Fore.CYAN + f"🔹 Registrar: {result.registrar}")
            print(Fore.CYAN + f"🔹 Creation Date: {result.creation_date}")
            print(Fore.CYAN + f"🔹 Expiration Date: {result.expiration_date}")
            print(Fore.CYAN + f"🔹 Name Servers: {result.name_servers}")
            print(Fore.CYAN + f"🔹 Emails: {result.emails}")
        else:
            print(Fore.YELLOW + "⚠️ No WHOIS data found.")
    except Exception as e:
        print(Fore.RED + f"[x] Error during WHOIS lookup: {e}")