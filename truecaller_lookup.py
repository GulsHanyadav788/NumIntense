import urllib.parse
from colorama import Fore, Style, init
from typing import List, Dict, Tuple, Optional
import requests
import time
import re
import json

# Initialize colorama
init(autoreset=True)

class AdvancedTruecallerLookup:
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.rate_limit_delay = 2  # seconds between requests

    def generate_truecaller_links(self, number: str) -> List[Tuple[str, str]]:
        """
        Generate multiple Truecaller and reverse lookup links
        
        Args:
            number: Phone number to lookup
            
        Returns:
            List of (source, url) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        links = [
            ("Truecaller Search", f"https://www.truecaller.com/search/{clean_number}"),
            ("Truecaller India", f"https://www.truecaller.com/search/in/{clean_number}"),
            ("Truecaller US", f"https://www.truecaller.com/search/us/{clean_number}"),
            ("Truecaller UK", f"https://www.truecaller.com/search/gb/{clean_number}"),
            ("Truecaller Web", f"https://truecaller.com/{clean_number}"),
            ("Truecaller App Link", f"https://truecaller.com/call/{clean_number}"),
        ]
        
        return links

    def generate_search_dorks(self, number: str) -> List[Tuple[str, str]]:
        """
        Generate comprehensive search dorks for Truecaller data
        
        Args:
            number: Phone number to search
            
        Returns:
            List of (search_type, url) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        dorks = [
            ("Truecaller Site Search", f'site:truecaller.com "{clean_number}"'),
            ("Truecaller Profile", f'"truecaller.com" "{clean_number}"'),
            ("Phone with Truecaller", f'"{clean_number}" "truecaller"'),
            ("Truecaller API", f'"{clean_number}" "truecaller api"'),
            ("Truecaller Leak", f'"{clean_number}" "truecaller" "leak"'),
            ("Truecaller Database", f'"{clean_number}" "truecaller" "database"'),
        ]
        
        # Generate search URLs for multiple engines
        search_engines = [
            ("Google", "https://www.google.com/search?q={}"),
            ("Bing", "https://www.bing.com/search?q={}"),
            ("DuckDuckGo", "https://duckduckgo.com/html/?q={}"),
            ("Yandex", "https://yandex.com/search/?text={}"),
        ]
        
        urls = []
        for dork_type, dork_query in dorks:
            for engine_name, base_url in search_engines:
                encoded_query = urllib.parse.quote(dork_query)
                url = base_url.format(encoded_query)
                urls.append((
                    f"{engine_name} - {dork_type}",
                    url
                ))
        
        return urls

    def check_third_party_apis(self, number: str) -> List[Tuple[str, str, Optional[Dict]]]:
        """
        Check multiple third-party Truecaller-like APIs
        
        Args:
            number: Phone number to check
            
        Returns:
            List of (api_name, api_url, response_data) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        apis = [
            {
                "name": "Numspy API",
                "url": f"https://api.numspy.io/v1/lookup?number={clean_number}",
                "headers": {"User-Agent": "NumIntensePro"}
            },
            {
                "name": "NumVerify",
                "url": f"https://api.numverify.com/v1/validate?number={clean_number}",
                "headers": {"User-Agent": "NumIntensePro"}
            },
            {
                "name": "AbstractAPI",
                "url": f"https://phonevalidation.abstractapi.com/v1/?phone={clean_number}",
                "headers": {"User-Agent": "NumIntensePro"}
            },
        ]
        
        results = []
        for api in apis:
            try:
                response = self.session.get(
                    api["url"], 
                    headers=api.get("headers", {}),
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results.append((api["name"], api["url"], data))
                else:
                    results.append((api["name"], api["url"], None))
                    
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                results.append((api["name"], api["url"], f"Error: {str(e)}"))
        
        return results

    def generate_alternative_lookup_sites(self, number: str) -> List[Tuple[str, str]]:
        """
        Generate alternative reverse phone lookup sites
        
        Args:
            number: Phone number to lookup
            
        Returns:
            List of (site_name, url) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        sites = [
            ("SpyDialer", f"https://www.spydialer.com/default.aspx?phone={clean_number}"),
            ("WhitePages", f"https://www.whitepages.com/phone/{clean_number}"),
            ("AnyWho", f"https://www.anywho.com/phone/{clean_number}"),
            ("411", f"https://www.411.com/phone/{clean_number}"),
            ("ZabaSearch", f"https://www.zabasearch.com/phone/{clean_number}"),
            ("NumberGuru", f"https://www.numberguru.com/phone/{clean_number}"),
            ("CallerCenter", f"https://callercenter.com/{clean_number}"),
            ("PhoneHistory", f"https://www.phonehistory.com/{clean_number}"),
            ("WhoCallsMe", f"https://whocallsme.com/Phone-Number.aspx/{clean_number}"),
            ("SyncMe", f"https://sync.me/search/?number={clean_number}"),
            ("EveryCaller", f"https://everycaller.com/phone-number/{clean_number}"),
        ]
        
        return sites

    def parse_api_response(self, api_name: str, data: Dict) -> Dict[str, str]:
        """
        Parse API response data into standardized format
        
        Args:
            api_name: Name of the API
            data: API response data
            
        Returns:
            Dictionary of parsed information
        """
        parsed = {}
        
        try:
            if api_name == "Numspy API":
                parsed.update({
                    "Name": data.get("name", "Not found"),
                    "Carrier": data.get("carrier", "Not found"),
                    "Location": data.get("location", "Not found"),
                    "Timezone": data.get("timezone", "Not found"),
                    "Valid": data.get("valid", "Unknown"),
                })
                
            elif api_name == "NumVerify":
                parsed.update({
                    "Valid": data.get("valid", "Unknown"),
                    "Number": data.get("international_format", "Not found"),
                    "Country": data.get("country_name", "Not found"),
                    "Location": data.get("location", "Not found"),
                    "Carrier": data.get("carrier", "Not found"),
                    "Line Type": data.get("line_type", "Not found"),
                })
                
            elif api_name == "AbstractAPI":
                parsed.update({
                    "Valid": data.get("valid", "Unknown"),
                    "Number": data.get("format", {}).get("international", "Not found"),
                    "Country": data.get("country", {}).get("name", "Not found"),
                    "Location": data.get("location", "Not found"),
                    "Carrier": data.get("carrier", "Not found"),
                    "Type": data.get("type", "Not found"),
                })
                
        except Exception as e:
            parsed["Error"] = f"Parse error: {str(e)}"
        
        return parsed

    def display_truecaller_links(self, number: str, links: List[Tuple[str, str]]) -> None:
        """
        Display Truecaller direct links
        
        Args:
            number: Phone number being checked
            links: List of Truecaller links
        """
        print(Fore.CYAN + f"\n{'='*80}")
        print(Fore.CYAN + f"📞 TRUECALLER LOOKUP FOR: {number}")
        print(Fore.CYAN + f"{'='*80}")
        
        print(Fore.YELLOW + f"\n[🔗] Direct Truecaller Links:")
        for i, (source, url) in enumerate(links, 1):
            print(Fore.GREEN + f"  {i}. {source}")
            print(Fore.WHITE + f"     {url}")

    def display_api_results(self, api_results: List[Tuple[str, str, Optional[Dict]]]) -> None:
        """
        Display API lookup results
        
        Args:
            api_results: List of API results
        """
        print(Fore.MAGENTA + f"\n[🔍] API Lookup Results:")
        
        successful_lookups = 0
        
        for api_name, api_url, data in api_results:
            if data and isinstance(data, dict):
                successful_lookups += 1
                print(Fore.GREEN + f"\n  ✅ {api_name}:")
                
                parsed_data = self.parse_api_response(api_name, data)
                for key, value in parsed_data.items():
                    if value and value != "Not found" and value != "Unknown":
                        print(Fore.WHITE + f"     {key}: {value}")
                        
            elif data and isinstance(data, str):
                print(Fore.RED + f"\n  ❌ {api_name}: {data}")
            else:
                print(Fore.YELLOW + f"\n  ⚠️  {api_name}: No data returned")
        
        if successful_lookups == 0:
            print(Fore.RED + f"\n  💡 Tip: API lookups may require valid API keys for full functionality")

    def display_search_dorks(self, search_dorks: List[Tuple[str, str]]) -> None:
        """
        Display generated search dorks
        
        Args:
            search_dorks: List of search dorks
        """
        print(Fore.YELLOW + f"\n[🎯] Search Engine Dorks:")
        
        # Group by search engine
        engines = {}
        for dork_name, url in search_dorks:
            engine = dork_name.split(' - ')[0]
            dork_type = ' - '.join(dork_name.split(' - ')[1:])
            
            if engine not in engines:
                engines[engine] = []
            engines[engine].append((dork_type, url))
        
        for engine, dorks in engines.items():
            print(Fore.CYAN + f"\n  {engine}:")
            for dork_type, url in dorks[:2]:  # Show first 2 per engine
                print(Fore.GREEN + f"    • {dork_type}")
                print(Fore.WHITE + f"      {url}")

    def display_alternative_sites(self, alt_sites: List[Tuple[str, str]]) -> None:
        """
        Display alternative lookup sites
        
        Args:
            alt_sites: List of alternative sites
        """
        print(Fore.BLUE + f"\n[🌐] Alternative Reverse Lookup Sites:")
        
        for i, (site_name, url) in enumerate(alt_sites[:8], 1):  # Show first 8
            print(Fore.GREEN + f"  {i}. {site_name}")
            print(Fore.WHITE + f"     {url}")
        
        if len(alt_sites) > 8:
            print(Fore.YELLOW + f"     ... and {len(alt_sites) - 8} more sites")

    def save_truecaller_report(self, number: str, truecaller_links: List[Tuple[str, str]], 
                             api_results: List[Tuple[str, str, Optional[Dict]]],
                             search_dorks: List[Tuple[str, str]], 
                             alt_sites: List[Tuple[str, str]], filename: str = None) -> None:
        """
        Save comprehensive Truecaller report to file
        
        Args:
            number: Phone number checked
            truecaller_links: List of Truecaller links
            api_results: List of API results
            search_dorks: List of search dorks
            alt_sites: List of alternative sites
            filename: Output filename
        """
        if filename is None:
            filename = f"truecaller_lookup_{number.replace('+', '')}.txt"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"TRUECALLER OSINT REPORT\n")
                f.write(f"Phone Number: {number}\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # Truecaller links
                f.write("DIRECT TRUECALLER LINKS:\n")
                f.write("-" * 40 + "\n")
                for source, url in truecaller_links:
                    f.write(f"  {source}: {url}\n")
                f.write("\n")
                
                # API Results
                f.write("API LOOKUP RESULTS:\n")
                f.write("-" * 40 + "\n")
                for api_name, api_url, data in api_results:
                    f.write(f"  {api_name}:\n")
                    f.write(f"    URL: {api_url}\n")
                    if data and isinstance(data, dict):
                        parsed_data = self.parse_api_response(api_name, data)
                        for key, value in parsed_data.items():
                            f.write(f"    {key}: {value}\n")
                    else:
                        f.write(f"    Result: No data available\n")
                    f.write("\n")
                
                # Search dorks
                f.write("SEARCH DORKS:\n")
                f.write("-" * 40 + "\n")
                for dork_name, url in search_dorks:
                    f.write(f"  {dork_name}: {url}\n")
                f.write("\n")
                
                # Alternative sites
                f.write("ALTERNATIVE LOOKUP SITES:\n")
                f.write("-" * 40 + "\n")
                for site_name, url in alt_sites:
                    f.write(f"  {site_name}: {url}\n")
                f.write("\n")
                
                # Legal disclaimer
                f.write("LEGAL DISCLAIMER:\n")
                f.write("-" * 40 + "\n")
                f.write("This report is for educational and authorized investigations only.\n")
                f.write("Respect privacy laws and terms of service of the listed platforms.\n")
                f.write("Some APIs may require proper authentication and paid subscriptions.\n")
            
            print(Fore.GREEN + f"[💾] Truecaller report saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"[❌] Error saving Truecaller report: {e}")

    def truecaller_lookup(self, number: str, save_report: bool = False, use_apis: bool = True) -> Dict:
        """
        Comprehensive Truecaller lookup function
        
        Args:
            number: Phone number to investigate
            save_report: Whether to save report to file
            use_apis: Whether to use third-party APIs
            
        Returns:
            Dictionary with all generated data
        """
        print(Fore.CYAN + f"\n[📞] Starting comprehensive Truecaller lookup for: {number}")
        
        # Generate Truecaller links
        truecaller_links = self.generate_truecaller_links(number)
        
        # Generate search dorks
        search_dorks = self.generate_search_dorks(number)
        
        # Check third-party APIs
        api_results = []
        if use_apis:
            api_results = self.check_third_party_apis(number)
        
        # Generate alternative sites
        alt_sites = self.generate_alternative_lookup_sites(number)
        
        # Display results
        self.display_truecaller_links(number, truecaller_links)
        
        if use_apis:
            self.display_api_results(api_results)
        
        self.display_search_dorks(search_dorks)
        self.display_alternative_sites(alt_sites)
        
        # Save report if requested
        if save_report:
            self.save_truecaller_report(number, truecaller_links, api_results, search_dorks, alt_sites)
        
        # Legal disclaimer
        print(Fore.RED + "\n" + "="*80)
        print(Fore.RED + "[!] LEGAL DISCLAIMER:")
        print(Fore.RED + "    This tool aggregates publicly available reverse lookup services.")
        print(Fore.RED + "    Respect privacy laws and platform terms of service.")
        print(Fore.RED + "    Some APIs may require proper authentication for full access.")
        
        return {
            'truecaller_links': truecaller_links,
            'api_results': api_results,
            'search_dorks': search_dorks,
            'alternative_sites': alt_sites
        }

    def batch_truecaller_lookup(self, numbers: List[str], delay: float = 3.0) -> None:
        """
        Perform Truecaller lookup on multiple numbers
        
        Args:
            numbers: List of phone numbers to check
            delay: Delay between checks in seconds
        """
        print(Fore.CYAN + f"\n[📞] Starting batch Truecaller lookup for {len(numbers)} numbers...")
        
        for i, number in enumerate(numbers, 1):
            print(Fore.YELLOW + f"\n[{i}/{len(numbers)}] Checking: {number}")
            self.truecaller_lookup(number)
            
            if i < len(numbers):  # No delay after last check
                print(Fore.YELLOW + f"[⏳] Waiting {delay} seconds...")
                time.sleep(delay)


# Simplified function for basic usage (backward compatibility)
def truecaller_lookup(number: str) -> None:
    """
    Simplified Truecaller lookup function (backward compatible)
    
    Args:
        number: Phone number to check
    """
    print(Fore.CYAN + f"\n[📞] Truecaller Lookup for: {number}")
    
    try:
        # Original dork
        dork = f'intext:"{number}" site:truecaller.com'
        encoded_dork = urllib.parse.quote(dork)
        print(Fore.YELLOW + f"[🔍] Google Dork: https://www.google.com/search?q={encoded_dork}")

        # Original API call
        clean_number = number.replace('+', '').replace(' ', '')
        url = f"https://api.numspy.io/v1/lookup?number={clean_number}"
        headers = {"User-Agent": "NumIntensePro"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            name = data.get("name")
            if name:
                print(Fore.GREEN + f"[🧠] Name: {name}")
            else:
                print(Fore.YELLOW + "[ℹ️] No name found.")
        else:
            print(Fore.RED + "[!] Could not fetch Truecaller data.")
            
    except Exception as e:
        print(Fore.RED + f"[x] Error during lookup: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Create Truecaller lookup instance
    tc_lookup = AdvancedTruecallerLookup()
    
    # Advanced usage
    report = tc_lookup.truecaller_lookup("+919876543210", save_report=True, use_apis=True)
    
    # Batch check
    numbers = ["+919876543210", "+11234567890", "+441234567890"]
    tc_lookup.batch_truecaller_lookup(numbers, delay=5.0)
    
    # Or use simplified function (backward compatible)
    truecaller_lookup("+919876543210")