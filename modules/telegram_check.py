import urllib.parse
from colorama import Fore, Style, init
from typing import List, Dict, Tuple
import requests
import time
import re
import hashlib

# Initialize colorama
init(autoreset=True)

class AdvancedTelegramLookup:
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.rate_limit_delay = 2  # seconds between requests

    def generate_username_variations(self, number: str) -> List[str]:
        """
        Generate multiple possible Telegram username variations
        
        Args:
            number: Phone number to generate variations from
            
        Returns:
            List of possible usernames
        """
        # Clean the number
        clean_number = number.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        variations = []
        
        # Basic variations
        variations.extend([
            clean_number,  # +919876543210 -> 919876543210
            clean_number[-10:],  # Last 10 digits (without country code)
            f"user{clean_number}",
            f"user{clean_number[-10:]}",
            f"id{clean_number}",
            f"id{clean_number[-10:]}",
            f"tg{clean_number}",
            f"tg{clean_number[-10:]}",
            f"telegram{clean_number}",
            f"telegram{clean_number[-10:]}",
        ])
        
        # Country-specific variations
        if number.startswith('+91'):  # India
            without_country = clean_number[2:]  # Remove 91
            variations.extend([
                without_country,
                f"user{without_country}",
                f"id{without_country}",
            ])
        elif number.startswith('+1'):  # US/Canada
            without_country = clean_number[1:]  # Remove 1
            variations.extend([
                without_country,
                f"user{without_country}",
                f"id{without_country}",
            ])
        elif number.startswith('+44'):  # UK
            without_country = clean_number[2:]  # Remove 44
            variations.extend([
                without_country,
                f"user{without_country}",
                f"id{without_country}",
            ])
        
        # Hash-based variations (common pattern)
        md5_hash = hashlib.md5(clean_number.encode()).hexdigest()[:10]
        sha1_hash = hashlib.sha1(clean_number.encode()).hexdigest()[:10]
        
        variations.extend([
            f"user{md5_hash}",
            f"id{md5_hash}",
            f"user{sha1_hash}",
            f"id{sha1_hash}",
        ])
        
        # Remove duplicates and empty strings
        variations = list(set([v for v in variations if v.strip()]))
        return variations

    def generate_direct_links(self, username_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate direct Telegram links for username variations
        
        Args:
            username_variations: List of possible usernames
            
        Returns:
            List of (username, url) tuples
        """
        links = []
        
        for username in username_variations:
            links.append((
                username,
                f"https://t.me/{username}"
            ))
        
        return links

    def generate_osint_links(self, number: str) -> List[Tuple[str, str]]:
        """
        Generate OSINT and search engine links for Telegram investigation
        
        Args:
            number: Phone number to investigate
            
        Returns:
            List of (source, url) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        osint_sources = [
            ("Google Search", f"https://www.google.com/search?q=%22{clean_number}%22+telegram"),
            ("Google Site Search", f"https://www.google.com/search?q=site:t.me+%22{clean_number}%22"),
            ("Bing Search", f"https://www.bing.com/search?q=%22{clean_number}%22+telegram"),
            ("DuckDuckGo", f"https://duckduckgo.com/?q=%22{clean_number}%22+telegram"),
            ("Yandex", f"https://yandex.com/search/?text=%22{clean_number}%22+telegram"),
            
            ("Telegram Search Bots", "https://t.me/search"),
            ("Telegram Global Search", "https://t.me/explore"),
            ("Telegram Contacts", "https://t.me/contacts"),
            
            ("GitHub Telegram OSINT", "https://github.com/search?q=telegram+osint+tools"),
            ("Telegram Analytics", "https://tgstat.com/search"),
            ("Telegram Group Search", "https://t.me/search/channels"),
            
            ("Social Search", f"https://www.google.com/search?q=%22@{clean_number}%22+site:t.me"),
            ("Username Search", f"https://www.google.com/search?q=%22t.me/{clean_number}%22"),
        ]
        
        return osint_sources

    def generate_advanced_queries(self, number: str, username_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate advanced search queries for comprehensive investigation
        
        Args:
            number: Phone number
            username_variations: List of username variations
            
        Returns:
            List of (query_type, query) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        queries = []
        
        # Basic number queries
        queries.extend([
            ("Phone in Telegram", f'"{clean_number}" telegram'),
            ("Phone with @", f'"{clean_number}" "@" telegram'),
            ("t.me links", f'"{clean_number}" "t.me"'),
        ])
        
        # Username specific queries
        for username in username_variations[:5]:  # Use first 5 variations
            queries.extend([
                (f"Username: {username}", f'"{username}" telegram'),
                (f"t.me/{username}", f'"t.me/{username}"'),
                (f"@{username}", f'"@{username}"'),
            ])
        
        # Advanced OSINT queries
        advanced_queries = [
            ("Telegram API", f'"{clean_number}" "telegram.org"'),
            ("Telegram Contact", f'"{clean_number}" "contact" telegram'),
            ("Telegram Profile", f'"{clean_number}" "profile" telegram'),
            ("Telegram Channel", f'"{clean_number}" "channel" telegram'),
            ("Telegram Group", f'"{clean_number}" "group" telegram'),
            ("Telegram Bot", f'"{clean_number}" "bot" telegram'),
            ("Telegram Database", f'"{clean_number}" "database" telegram'),
            ("Telegram Leak", f'"{clean_number}" "leak" telegram'),
            ("Telegram Export", f'"{clean_number}" "export" telegram'),
        ]
        
        queries.extend(advanced_queries)
        
        return queries

    def check_telegram_public_data(self, number: str) -> List[Tuple[str, str]]:
        """
        Check public Telegram databases and directories
        
        Args:
            number: Phone number to check
            
        Returns:
            List of (database, url) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        public_sources = [
            ("Telegram Directory", "https://t.me/directory"),
            ("Telegram Store", "https://t.me/store"),
            ("Telegram FAQ", "https://telegram.org/faq"),
            ("Telegram Blog", "https://telegram.org/blog"),
            ("Telegram API", "https://core.telegram.org/"),
            
            ("TGStat", f"https://tgstat.com/search?q={clean_number}"),
            ("Telegram Group List", "https://tgram.io/"),
            ("Telegram Analytics", "https://telegramchannels.me/"),
            ("Telegram Channels", "https://tchannels.me/"),
            
            ("GitHub Telegram Tools", "https://github.com/topics/telegram-osint"),
            ("OSINT Framework", "https://osintframework.com/"),
        ]
        
        return public_sources

    def generate_search_urls(self, queries: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """
        Convert queries to search engine URLs
        
        Args:
            queries: List of (query_type, query) tuples
            
        Returns:
            List of (query_type, url) tuples
        """
        search_engines = [
            ("Google", "https://www.google.com/search?q={}"),
            ("Bing", "https://www.bing.com/search?q={}"),
            ("DuckDuckGo", "https://duckduckgo.com/html/?q={}"),
            ("Yandex", "https://yandex.com/search/?text={}"),
            ("Startpage", "https://www.startpage.com/sp/search?query={}"),
        ]
        
        urls = []
        
        for query_type, query in queries:
            for engine_name, base_url in search_engines:
                encoded_query = urllib.parse.quote(query)
                url = base_url.format(encoded_query)
                urls.append((
                    f"{engine_name} - {query_type}",
                    url
                ))
        
        return urls

    def display_telegram_links(self, number: str, direct_links: List[Tuple[str, str]]) -> None:
        """
        Display direct Telegram profile links
        
        Args:
            number: Phone number being checked
            direct_links: List of (username, url) tuples
        """
        print(Fore.CYAN + f"\n{'='*80}")
        print(Fore.CYAN + f"📱 TELEGRAM PROFILE LOOKUP FOR: {number}")
        print(Fore.CYAN + f"{'='*80}")
        
        print(Fore.YELLOW + f"\n[🔍] Direct Telegram Profile Links ({len(direct_links)} variations):")
        
        for i, (username, url) in enumerate(direct_links[:10], 1):  # Show first 10
            print(Fore.GREEN + f"  {i}. @{username}")
            print(Fore.WHITE + f"     {url}")
        
        if len(direct_links) > 10:
            print(Fore.YELLOW + f"     ... and {len(direct_links) - 10} more username variations")

    def display_osint_sources(self, osint_links: List[Tuple[str, str]]) -> None:
        """
        Display OSINT investigation sources
        
        Args:
            osint_links: List of (source, url) tuples
        """
        print(Fore.MAGENTA + f"\n[🎯] Telegram OSINT Investigation Sources:")
        
        for i, (source, url) in enumerate(osint_links, 1):
            print(Fore.GREEN + f"  {i}. {source}")
            print(Fore.WHITE + f"     {url}")

    def display_search_queries(self, search_urls: List[Tuple[str, str]]) -> None:
        """
        Display generated search queries
        
        Args:
            search_urls: List of (query_type, url) tuples
        """
        print(Fore.YELLOW + f"\n[🔎] Advanced Search Queries:")
        
        # Group by search engine
        engines = {}
        for query_name, url in search_urls:
            engine = query_name.split(' - ')[0]
            query_type = ' - '.join(query_name.split(' - ')[1:])
            
            if engine not in engines:
                engines[engine] = []
            engines[engine].append((query_type, url))
        
        for engine, queries in engines.items():
            print(Fore.CYAN + f"\n  {engine} Search:")
            for query_type, url in queries[:3]:  # Show first 3 per engine
                print(Fore.GREEN + f"    • {query_type}")
                print(Fore.WHITE + f"      {url}")
            
            if len(queries) > 3:
                print(Fore.YELLOW + f"      ... and {len(queries) - 3} more queries")

    def display_public_sources(self, public_sources: List[Tuple[str, str]]) -> None:
        """
        Display public Telegram data sources
        
        Args:
            public_sources: List of (source, url) tuples
        """
        print(Fore.BLUE + f"\n[📊] Public Telegram Data Sources:")
        
        for i, (source, url) in enumerate(public_sources, 1):
            print(Fore.GREEN + f"  {i}. {source}")
            print(Fore.WHITE + f"     {url}")

    def save_telegram_report(self, number: str, direct_links: List[Tuple[str, str]], 
                           osint_links: List[Tuple[str, str]], search_urls: List[Tuple[str, str]],
                           public_sources: List[Tuple[str, str]], filename: str = None) -> None:
        """
        Save comprehensive Telegram report to file
        
        Args:
            number: Phone number checked
            direct_links: List of direct profile links
            osint_links: List of OSINT sources
            search_urls: List of search queries
            public_sources: List of public data sources
            filename: Output filename
        """
        if filename is None:
            filename = f"telegram_lookup_{number.replace('+', '')}.txt"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"TELEGRAM OSINT REPORT\n")
                f.write(f"Phone Number: {number}\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # Direct links
                f.write("DIRECT TELEGRAM PROFILE LINKS:\n")
                f.write("-" * 40 + "\n")
                for username, url in direct_links:
                    f.write(f"  @{username}: {url}\n")
                f.write("\n")
                
                # OSINT sources
                f.write("OSINT INVESTIGATION SOURCES:\n")
                f.write("-" * 40 + "\n")
                for source, url in osint_links:
                    f.write(f"  {source}: {url}\n")
                f.write("\n")
                
                # Search queries
                f.write("ADVANCED SEARCH QUERIES:\n")
                f.write("-" * 40 + "\n")
                for query_name, url in search_urls:
                    f.write(f"  {query_name}: {url}\n")
                f.write("\n")
                
                # Public sources
                f.write("PUBLIC TELEGRAM DATA:\n")
                f.write("-" * 40 + "\n")
                for source, url in public_sources:
                    f.write(f"  {source}: {url}\n")
                f.write("\n")
                
                # Methodology
                f.write("METHODOLOGY:\n")
                f.write("-" * 40 + "\n")
                f.write("1. Username generation based on phone number patterns\n")
                f.write("2. Direct Telegram profile link testing\n")
                f.write("3. Search engine OSINT queries\n")
                f.write("4. Public Telegram directory checks\n")
                f.write("5. Advanced Telegram OSINT techniques\n\n")
                
                # Legal disclaimer
                f.write("LEGAL DISCLAIMER:\n")
                f.write("-" * 40 + "\n")
                f.write("This report is for educational and authorized investigations only.\n")
                f.write("Respect Telegram's Terms of Service and applicable privacy laws.\n")
                f.write("Unauthorized access or scraping may violate laws and platform policies.\n")
            
            print(Fore.GREEN + f"[💾] Telegram report saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"[❌] Error saving Telegram report: {e}")

    def telegram_lookup(self, number: str, save_report: bool = False, advanced: bool = True) -> Dict:
        """
        Comprehensive Telegram lookup function
        
        Args:
            number: Phone number to investigate
            save_report: Whether to save report to file
            advanced: Whether to include advanced techniques
            
        Returns:
            Dictionary with all generated data
        """
        print(Fore.CYAN + f"\n[🔍] Starting comprehensive Telegram lookup for: {number}")
        
        # Generate username variations
        username_variations = self.generate_username_variations(number)
        print(Fore.YELLOW + f"[📊] Generated {len(username_variations)} username variations")
        
        # Generate direct links
        direct_links = self.generate_direct_links(username_variations)
        
        # Generate OSINT links
        osint_links = self.generate_osint_links(number)
        
        # Generate advanced queries
        search_queries = self.generate_advanced_queries(number, username_variations)
        search_urls = self.generate_search_urls(search_queries)
        
        # Get public data sources
        public_sources = self.check_telegram_public_data(number)
        
        # Display results
        self.display_telegram_links(number, direct_links)
        self.display_osint_sources(osint_links)
        
        if advanced:
            self.display_search_queries(search_urls)
            self.display_public_sources(public_sources)
        
        # Save report if requested
        if save_report:
            self.save_telegram_report(number, direct_links, osint_links, search_urls, public_sources)
        
        # Legal disclaimer
        print(Fore.RED + "\n" + "="*80)
        print(Fore.RED + "[!] LEGAL DISCLAIMER:")
        print(Fore.RED + "    This tool is for educational and authorized security research only.")
        print(Fore.RED + "    Respect Telegram's Terms of Service and applicable privacy laws.")
        print(Fore.RED + "    Do not use for harassment, stalking, or illegal activities.")
        
        return {
            'username_variations': username_variations,
            'direct_links': direct_links,
            'osint_links': osint_links,
            'search_urls': search_urls,
            'public_sources': public_sources
        }

    def batch_telegram_lookup(self, numbers: List[str], delay: float = 3.0) -> None:
        """
        Perform Telegram lookup on multiple numbers
        
        Args:
            numbers: List of phone numbers to check
            delay: Delay between checks in seconds
        """
        print(Fore.CYAN + f"\n[🔍] Starting batch Telegram lookup for {len(numbers)} numbers...")
        
        for i, number in enumerate(numbers, 1):
            print(Fore.YELLOW + f"\n[{i}/{len(numbers)}] Checking: {number}")
            self.telegram_lookup(number)
            
            if i < len(numbers):  # No delay after last check
                print(Fore.YELLOW + f"[⏳] Waiting {delay} seconds...")
                time.sleep(delay)


# Simplified function for basic usage (backward compatibility)
def telegram_lookup(number: str) -> None:
    """
    Simplified Telegram lookup function (backward compatible)
    
    Args:
        number: Phone number to check
    """
    username_guess = number.replace("+", "")
    print(Fore.CYAN + f"\n[🔍] Telegram Profile Search: https://t.me/{username_guess}")
    
    # Additional basic links for backward compatibility
    basic_links = [
        f"https://t.me/user{username_guess}",
        f"https://t.me/id{username_guess}",
    ]
    
    for link in basic_links:
        print(Fore.GREEN + f"[Link] {link}")


# Example usage and testing
if __name__ == "__main__":
    # Create Telegram lookup instance
    tg_lookup = AdvancedTelegramLookup()
    
    # Advanced usage
    report = tg_lookup.telegram_lookup("+919876543210", save_report=True, advanced=True)
    
    # Batch check
    numbers = ["+919876543210", "+11234567890", "+441234567890"]
    tg_lookup.batch_telegram_lookup(numbers, delay=5.0)
    
    # Or use simplified function (backward compatible)
    telegram_lookup("+919876543210")