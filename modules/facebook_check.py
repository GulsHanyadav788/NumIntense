# Enhanced Facebook OSINT Module
import urllib.parse
from colorama import Fore, Style, init
from typing import List, Dict, Tuple
import requests
import time
import re

init(autoreset=True)

class AdvancedFacebookOSINT:
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.rate_limit_delay = 2

    def generate_facebook_dorks(self, number: str) -> List[Dict[str, str]]:
        clean_number = number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        
        dorks = [
            {"name": "Basic Phone Search", "query": f'intext:"{number}" site:facebook.com'},
            {"name": "Phone without spaces", "query": f'intext:"{clean_number}" site:facebook.com'},
            {"name": "Phone in profiles", "query": f'"mobile phones" "{number}" site:facebook.com'},
            {"name": "Phone in about sections", "query": f'"about" "{number}" site:facebook.com'},
            {"name": "Phone in contact info", "query": f'"contact" "{number}" site:facebook.com'}
        ]
        
        if number.startswith('+'):
            without_plus = number[1:]
            dorks.append({"name": "International without +", "query": f'intext:"{without_plus}" site:facebook.com'})
        
        return dorks

    def generate_search_links(self, dorks: List[Dict[str, str]]) -> Dict[str, List[str]]:
        search_engines = {
            "Google": "https://www.google.com/search?q={}",
            "DuckDuckGo": "https://duckduckgo.com/html/?q={}",
            "Bing": "https://www.bing.com/search?q={}",
            "Yandex": "https://yandex.com/search/?text={}",
            "Startpage": "https://www.startpage.com/sp/search?query={}"
        }
        
        links = {}
        
        for engine, base_url in search_engines.items():
            engine_links = []
            for dork in dorks:
                encoded_query = urllib.parse.quote(dork["query"])
                url = base_url.format(encoded_query)
                engine_links.append({"name": dork["name"], "url": url})
            links[engine] = engine_links
            
        return links

    def facebook_direct_search(self, number: str) -> List[str]:
        clean_number = number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        direct_urls = [
            f"https://www.facebook.com/search/top/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/people/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/pages/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/groups/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/places/?q={urllib.parse.quote(clean_number)}"
        ]
        
        return direct_urls

    def display_results(self, number: str, search_links: Dict[str, List[str]], direct_urls: List[str]) -> None:
        print(Fore.MAGENTA + f"\n{'='*70}")
        print(Fore.MAGENTA + f"📱 FACEBOOK OSINT CHECK: {number}")
        print(Fore.MAGENTA + f"{'='*70}")
        
        print(Fore.CYAN + "\n[🔗] Direct Facebook Searches:")
        for i, url in enumerate(direct_urls, 1):
            print(Fore.GREEN + f"  {i}. {url}")
        
        print(Fore.CYAN + f"\n[🎯] Search Engine Dorks:")
        for engine, dorks in search_links.items():
            print(Fore.YELLOW + f"\n  ┌─ {engine}")
            for dork_info in dorks[:3]:
                print(Fore.GREEN + f"  ├─ {dork_info['name']}")
                print(Fore.WHITE + f"  │  {dork_info['url']}")
            if len(dorks) > 3:
                print(Fore.YELLOW + f"  └─ ... and {len(dorks) - 3} more dorks")
            else:
                print(Fore.YELLOW + "  └─" + "─" * 50)

    def facebook_check(self, number: str, save_output: bool = False, advanced: bool = False) -> None:
        print(Fore.CYAN + f"\n[🔍] Starting Facebook OSINT check for: {number}")
        
        dorks = self.generate_facebook_dorks(number)
        search_links = self.generate_search_links(dorks)
        direct_urls = self.facebook_direct_search(number)
        
        self.display_results(number, search_links, direct_urls)
        
        if save_output:
            self.save_results(number, search_links, direct_urls)
        
        print(Fore.RED + "\n" + "="*70)
        print(Fore.RED + "[!] LEGAL DISCLAIMER: For educational and authorized research only.")

    def save_results(self, number: str, search_links: Dict, direct_urls: List[str], filename: str = None) -> None:
        if filename is None:
            filename = f"facebook_osint_{number.replace('+', '')}.txt"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Facebook OSINT Report for: {number}\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("DIRECT FACEBOOK SEARCHES:\n")
                for url in direct_urls:
                    f.write(f"{url}\n")
                
                f.write("\nSEARCH ENGINE DORKS:\n")
                for engine, dorks in search_links.items():
                    f.write(f"\n{engine}:\n")
                    for dork_info in dorks:
                        f.write(f"  {dork_info['name']}: {dork_info['url']}\n")
            
            print(Fore.GREEN + f"[💾] Results saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"\n[❌] Error saving results: {e}")

# Simplified function for basic usage
def facebook_check(number: str, save_output: bool = False) -> None:
    fb_osint = AdvancedFacebookOSINT()
    fb_osint.facebook_check(number, save_output)