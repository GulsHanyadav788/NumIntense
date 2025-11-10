#!/usr/bin/env python3
"""
Advanced Dork Generation Module
Description: Generate comprehensive Google dorks for OSINT
Version: 3.1.0
"""

import urllib.parse
from colorama import Fore, Style, init

init(autoreset=True)

class DorkGenerator:
    def __init__(self):
        self.search_engines = {
            "Google": "https://www.google.com/search?q={}",
            "Bing": "https://www.bing.com/search?q={}",
            "DuckDuckGo": "https://duckduckgo.com/html/?q={}",
            "Yandex": "https://yandex.com/search/?text={}",
        }

    def generate_phone_dorks(self, number):
        """Generate phone number specific dorks"""
        clean_num = number.replace('+', '').replace(' ', '')
        
        dorks = {
            "Basic Phone Search": f'intext:"{number}"',
            "Social Media": f'intext:"{number}" site:facebook.com OR site:instagram.com OR site:twitter.com',
            "Documents": f'"{number}" filetype:pdf OR filetype:doc OR filetype:xls',
            "Paste Sites": f'"{number}" site:pastebin.com OR site:justpaste.it',
            "Forums": f'"{number}" site:reddit.com OR site:quora.com',
            "Business Listings": f'"{number}" site:yellowpages.com OR site:whitepages.com',
            "Telegram": f'"{number}" site:t.me OR site:telegram.me',
        }
        
        return dorks

    def generate_email_dorks(self, email):
        """Generate email specific dorks"""
        dorks = {
            "Basic Email": f'"{email}"',
            "Social Media": f'"{email}" site:facebook.com OR site:linkedin.com',
            "Data Breaches": f'"{email}" "password" OR "breach" OR "leak"',
            "Documents": f'"{email}" filetype:pdf OR filetype:doc',
            "GitHub": f'"{email}" site:github.com',
            "Paste Sites": f'"{email}" site:pastebin.com',
        }
        
        return dorks

    def generate_domain_dorks(self, domain):
        """Generate domain specific dorks"""
        dorks = {
            "Site Search": f'site:{domain}',
            "Subdomains": f'site:*.{domain}',
            "Documents": f'site:{domain} filetype:pdf OR filetype:doc OR filetype:xls',
            "Admin Pages": f'site:{domain} intitle:"admin" OR intitle:"login"',
            "Config Files": f'site:{domain} ext:env OR ext:config OR ext:sql',
            "Backup Files": f'site:{domain} ext:bak OR ext:backup OR ext:old',
        }
        
        return dorks

    def display_dorks(self, query, dorks, query_type):
        """Display generated dorks"""
        print(Fore.CYAN + f"\n[🎯] Advanced Dorks: {query}")
        print(Fore.CYAN + "─" * 50)
        print(Fore.YELLOW + f"Query Type: {query_type}")
        print(Fore.YELLOW + f"Total Dorks: {len(dorks)}")
        
        for engine_name, base_url in self.search_engines.items():
            print(f"\n{Fore.MAGENTA}🔍 {engine_name}:")
            
            for dork_name, dork_query in list(dorks.items())[:3]:  # Show first 3 per engine
                encoded = urllib.parse.quote(dork_query)
                url = base_url.format(encoded)
                print(f"    {Fore.GREEN}• {dork_name}")
                print(f"        {Fore.CYAN}{url}")
            
            if len(dorks) > 3:
                print(f"    {Fore.YELLOW}• ... and {len(dorks) - 3} more dorks")

    def generate_all_dorks(self, query, query_type="phone"):
        """Generate all dorks based on query type"""
        if query_type == "phone":
            dorks = self.generate_phone_dorks(query)
        elif query_type == "email":
            dorks = self.generate_email_dorks(query)
        elif query_type == "domain":
            dorks = self.generate_domain_dorks(query)
        else:
            dorks = {"Basic": f'"{query}"'}
            
        self.display_dorks(query, dorks, query_type)
        return dorks

    def save_dorks(self, query, dorks, filename=None):
        """Save dorks to file"""
        if filename is None:
            filename = f"dorks_{query.replace('@', '_').replace('.', '_')}.txt"
            
        try:
            with open(filename, 'w') as f:
                f.write(f"Dork Generation Report\n")
                f.write(f"Query: {query}\n")
                f.write("=" * 50 + "\n\n")
                
                for dork_name, dork_query in dorks.items():
                    f.write(f"{dork_name}:\n")
                    f.write(f"  {dork_query}\n\n")
                    
                    for engine_name, base_url in self.search_engines.items():
                        encoded = urllib.parse.quote(dork_query)
                        url = base_url.format(encoded)
                        f.write(f"  {engine_name}: {url}\n")
                    f.write("\n")
                    
            print(Fore.GREEN + f"[💾] Dorks saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"[❌] Error saving dorks: {e}")

def generate_dorks(query, query_type="phone", save=False):
    """Main function to generate dorks"""
    generator = DorkGenerator()
    dorks = generator.generate_all_dorks(query, query_type)
    
    if save:
        generator.save_dorks(query, dorks)
    
    return dorks

# Command line usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query_type = "phone"
        if len(sys.argv) > 2:
            query_type = sys.argv[2]
        generate_dorks(sys.argv[1], query_type, save=True)
    else:
        print(Fore.RED + "Usage: python advanced_dorks.py query [phone|email|domain]")