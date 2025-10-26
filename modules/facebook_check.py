import urllib.parse
from colorama import Fore, Style, init
import requests
import time
from typing import List, Dict

# Initialize colorama
init(autoreset=True)

class FacebookOSINT:
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.rate_limit_delay = 2  # seconds between requests

    def generate_facebook_dorks(self, number: str) -> List[Dict[str, str]]:
        """
        Generate multiple Facebook-specific search dorks
        
        Args:
            number: Phone number to investigate
            
        Returns:
            List of dork dictionaries with name and query
        """
        # Clean the number for different formats
        clean_number = number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
        
        dorks = []
        
        # Basic dorks
        dorks.extend([
            {
                "name": "Basic Phone Search",
                "query": f'intext:"{number}" site:facebook.com'
            },
            {
                "name": "Phone without spaces", 
                "query": f'intext:"{clean_number}" site:facebook.com'
            },
            {
                "name": "Phone in profiles",
                "query": f'"mobile phones" "{number}" site:facebook.com'
            },
            {
                "name": "Phone in about sections",
                "query": f'"about" "{number}" site:facebook.com'
            },
            {
                "name": "Phone in contact info",
                "query": f'"contact" "{number}" site:facebook.com'
            }
        ])
        
        # International format variations
        if number.startswith('+'):
            without_plus = number[1:]
            dorks.extend([
                {
                    "name": "International without +",
                    "query": f'intext:"{without_plus}" site:facebook.com'
                }
            ])
        
        # Country code specific dorks
        if number.startswith('+91'):  # India
            without_country = number[3:]
            dorks.append({
                "name": "Indian number without country code",
                "query": f'intext:"{without_country}" site:facebook.com'
            })
        elif number.startswith('+1'):  # US/Canada
            without_country = number[2:]
            dorks.append({
                "name": "US/Canada without country code", 
                "query": f'intext:"{without_country}" site:facebook.com'
            })
        
        return dorks

    def generate_search_links(self, dorks: List[Dict[str, str]]) -> Dict[str, List[str]]:
        """
        Generate search links for multiple search engines
        
        Args:
            dorks: List of dork dictionaries
            
        Returns:
            Dictionary with search engine names as keys and lists of URLs as values
        """
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
                engine_links.append({
                    "name": dork["name"],
                    "url": url
                })
            links[engine] = engine_links
            
        return links

    def facebook_direct_search(self, number: str) -> List[str]:
        """
        Generate direct Facebook search URLs
        
        Args:
            number: Phone number to search
            
        Returns:
            List of direct Facebook search URLs
        """
        clean_number = number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        direct_urls = [
            f"https://www.facebook.com/search/top/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/people/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/pages/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/groups/?q={urllib.parse.quote(clean_number)}",
            f"https://www.facebook.com/search/places/?q={urllib.parse.quote(clean_number)}"
        ]
        
        return direct_urls

    def check_facebook_public_pages(self, number: str) -> None:
        """
        Check for phone number in Facebook public pages and directories
        
        Args:
            number: Phone number to check
        """
        print(Fore.YELLOW + "\n[🔍] Checking Facebook Public Directories...")
        
        public_checks = [
            ("Facebook People Search", f"https://www.facebook.com/public?query={urllib.parse.quote(number)}"),
            ("Facebook Directory", "https://www.facebook.com/directory/people/"),
            ("Facebook Mobile Search", f"https://m.facebook.com/search/top/?q={urllib.parse.quote(number)}")
        ]
        
        for name, url in public_checks:
            print(Fore.CYAN + f"  {name}: {url}")

    def display_results(self, number: str, search_links: Dict[str, List[str]], direct_urls: List[str]) -> None:
        """
        Display formatted results
        
        Args:
            number: Original phone number
            search_links: Generated search links
            direct_urls: Direct Facebook search URLs
        """
        print(Fore.MAGENTA + f"\n{'='*70}")
        print(Fore.MAGENTA + f"📱 FACEBOOK OSINT CHECK: {number}")
        print(Fore.MAGENTA + f"{'='*70}")
        
        # Display direct Facebook searches
        print(Fore.CYAN + "\n[🔗] Direct Facebook Searches:")
        for i, url in enumerate(direct_urls, 1):
            print(Fore.GREEN + f"  {i}. {url}")
        
        # Display search engine dorks
        print(Fore.CYAN + f"\n[🎯] Search Engine Dorks:")
        for engine, dorks in search_links.items():
            print(Fore.YELLOW + f"\n  ┌─ {engine}")
            for dork_info in dorks[:3]:  # Show first 3 per engine
                print(Fore.GREEN + f"  ├─ {dork_info['name']}")
                print(Fore.WHITE + f"  │  {dork_info['url']}")
            if len(dorks) > 3:
                print(Fore.YELLOW + f"  └─ ... and {len(dorks) - 3} more dorks")
            else:
                print(Fore.YELLOW + "  └─" + "─" * 50)

    def advanced_facebook_checks(self, number: str) -> None:
        """
        Perform advanced Facebook-specific checks
        
        Args:
            number: Phone number to investigate
        """
        print(Fore.CYAN + "\n[⚡] Advanced Facebook OSINT Techniques:")
        
        advanced_methods = [
            "📊 Graph Search Queries",
            "👥 Mutual Friends Analysis", 
            "📷 Photo Metadata Checking",
            "🏷️ Tagged Photos Review",
            "📅 Event Participation",
            "👥 Group Memberships",
            "📍 Location Check-ins",
            "🕒 Timeline Analysis"
        ]
        
        for method in advanced_methods:
            print(Fore.YELLOW + f"  • {method}")
        
        print(Fore.RED + "\n[⚠️]  Note: Advanced techniques may require:")
        print(Fore.RED + "     - Valid Facebook account")
        print(Fore.RED + "     - Appropriate permissions")
        print(Fore.RED + "     - Legal authorization")

    def save_results(self, number: str, search_links: Dict, direct_urls: List[str], filename: str = None) -> None:
        """
        Save generated links to a file
        
        Args:
            number: Phone number searched
            search_links: Generated search links
            direct_urls: Direct Facebook URLs
            filename: Output filename
        """
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
            
            print(Fore.GREEN + f"\n[💾] Results saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"\n[❌] Error saving results: {e}")

    def facebook_check(self, number: str, save_output: bool = False, advanced: bool = False) -> None:
        """
        Comprehensive Facebook OSINT check
        
        Args:
            number: Phone number to investigate
            save_output: Whether to save results to file
            advanced: Whether to show advanced techniques
        """
        print(Fore.CYAN + f"\n[🔍] Starting Facebook OSINT check for: {number}")
        
        # Generate dorks
        dorks = self.generate_facebook_dorks(number)
        
        # Generate search links
        search_links = self.generate_search_links(dorks)
        
        # Generate direct Facebook URLs
        direct_urls = self.facebook_direct_search(number)
        
        # Display results
        self.display_results(number, search_links, direct_urls)
        
        # Public directory checks
        self.check_facebook_public_pages(number)
        
        # Advanced techniques
        if advanced:
            self.advanced_facebook_checks(number)
        
        # Save results if requested
        if save_output:
            self.save_results(number, search_links, direct_urls)
        
        # Legal disclaimer
        print(Fore.RED + "\n" + "="*70)
        print(Fore.RED + "[!] LEGAL DISCLAIMER:")
        print(Fore.RED + "    This tool is for educational and authorized security research only.")
        print(Fore.RED + "    Respect privacy laws and Facebook's Terms of Service.")
        print(Fore.RED + "    Unauthorized use may violate laws and platform policies.")

    def batch_facebook_check(self, numbers: List[str], delay: float = 3.0) -> None:
        """
        Perform Facebook check on multiple numbers
        
        Args:
            numbers: List of phone numbers to check
            delay: Delay between checks in seconds
        """
        print(Fore.CYAN + f"\n[🔍] Starting batch Facebook check for {len(numbers)} numbers...")
        
        for i, number in enumerate(numbers, 1):
            print(Fore.YELLOW + f"\n[{i}/{len(numbers)}] Checking: {number}")
            self.facebook_check(number)
            
            if i < len(numbers):  # No delay after last check
                print(Fore.YELLOW + f"[⏳] Waiting {delay} seconds...")
                time.sleep(delay)


# Simplified function for basic usage (backward compatibility)
def facebook_check(number: str, save_output: bool = False) -> None:
    """
    Simplified Facebook check function (backward compatible)
    
    Args:
        number: Phone number to investigate
        save_output: Whether to save results to file
    """
    fb_osint = FacebookOSINT()
    fb_osint.facebook_check(number, save_output)


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    fb_osint = FacebookOSINT()
    
    # Single check
    fb_osint.facebook_check("+919876543210", save_output=True, advanced=True)
    
    # Batch check
    numbers = ["+919876543210", "+11234567890"]
    fb_osint.batch_facebook_check(numbers)
    
    # Or use simplified function
    facebook_check("+919876543210")