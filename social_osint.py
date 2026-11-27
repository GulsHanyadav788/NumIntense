#!/usr/bin/env python3
"""
Social Media OSINT Module
Description: Comprehensive social media intelligence
Version: 3.1.0
"""

import requests
from colorama import Fore, Style, init

init(autoreset=True)

class SocialOSINT:
    def __init__(self):
        self.platforms = {
            "Facebook": {
                "search": "https://www.facebook.com/search/top/?q={}",
                "people": "https://www.facebook.com/search/people/?q={}",
                "pages": "https://www.facebook.com/search/pages/?q={}",
            },
            "Instagram": {
                "search": "https://www.instagram.com/search/top/?q={}",
                "explore": "https://www.instagram.com/explore/tags/{}/",
            },
            "Twitter": {
                "search": "https://twitter.com/search?q={}",
                "users": "https://twitter.com/search?q={}&f=user",
            },
            "LinkedIn": {
                "search": "https://www.linkedin.com/search/results/all/?keywords={}",
                "people": "https://www.linkedin.com/search/results/people/?keywords={}",
            },
            "Telegram": {
                "search": "https://t.me/{}",
                "global": "https://t.me/explore",
            },
            "YouTube": {
                "search": "https://www.youtube.com/results?search_query={}",
                "channel": "https://www.youtube.com/c/{}",
            },
            "Reddit": {
                "search": "https://www.reddit.com/search/?q={}",
                "users": "https://www.reddit.com/user/{}",
            },
            "GitHub": {
                "search": "https://github.com/search?q={}",
                "users": "https://github.com/{}",
            }
        }

    def generate_links(self, query, query_type="phone"):
        """Generate social media search links"""
        print(Fore.CYAN + f"\n[🔍] Social Media OSINT: {query}")
        print(Fore.CYAN + "─" * 50)
        
        clean_query = query.replace('+', '').replace(' ', '')
        
        for platform, searches in self.platforms.items():
            print(f"\n{Fore.YELLOW}📱 {platform}:")
            for search_type, url_template in searches.items():
                if query_type == "phone":
                    url = url_template.format(clean_query)
                else:
                    url = url_template.format(requests.utils.quote(query))
                print(f"    {Fore.GREEN}• {search_type.title()}: {Fore.CYAN}{url}")

    def username_search(self, username):
        """Search for username across platforms"""
        print(Fore.CYAN + f"\n[👤] Username Search: @{username}")
        print(Fore.CYAN + "─" * 50)
        
        sites = {
            "WhatsApp": f"https://wa.me/{username}",
            "Telegram": f"https://t.me/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://reddit.com/user/{username}",
            "YouTube": f"https://youtube.com/@{username}",
            "TikTok": f"https://tiktok.com/@{username}",
            "Snapchat": f"https://snapchat.com/add/{username}",
        }
        
        for site, url in sites.items():
            print(f"    {Fore.GREEN}• {site}: {Fore.CYAN}{url}")

    def advanced_search(self, query):
        """Advanced social media search techniques"""
        print(Fore.CYAN + f"\n[🎯] Advanced Search Techniques:")
        print(Fore.CYAN + "─" * 50)
        
        techniques = {
            "Google Dork": f'site:facebook.com "{query}"',
            "Google Images": f'https://www.google.com/search?tbm=isch&q={query}',
            "Reverse Image": "https://images.google.com/",
            "People Search": f'https://www.google.com/search?q="{query}"+person',
        }
        
        for tech, search in techniques.items():
            if tech == "Google Dork":
                encoded = requests.utils.quote(search)
                url = f"https://www.google.com/search?q={encoded}"
            else:
                url = search
            print(f"    {Fore.GREEN}• {tech}: {Fore.CYAN}{url}")

    def run_social_scan(self, query, query_type="phone"):
        """Run complete social media scan"""
        print(Fore.CYAN + f"\n[🚀] Starting social media intelligence...")
        
        self.generate_links(query, query_type)
        
        if query_type == "username":
            self.username_search(query)
        elif query_type == "phone":
            # Try to extract possible username from phone
            clean_phone = query.replace('+', '').replace(' ', '')
            possible_username = clean_phone[-10:]  # Last 10 digits
            self.username_search(possible_username)
            
        self.advanced_search(query)
        
        print(f"\n{Fore.GREEN}[✅] Social media scan completed!")

def run_social_scan(query, query_type="phone"):
    """Main function to run social media scan"""
    scanner = SocialOSINT()
    scanner.run_social_scan(query, query_type)

# Command line usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query_type = "phone"
        if len(sys.argv) > 2:
            query_type = sys.argv[2]
        run_social_scan(sys.argv[1], query_type)
    else:
        print(Fore.RED + "Usage: python social_osint.py query [phone|username|email]")