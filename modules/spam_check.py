import urllib.parse
from colorama import Fore, Style, init
from typing import List, Dict, Tuple
import requests
import time
import re

# Initialize colorama
init(autoreset=True)

class AdvancedSpamChecker:
    def __init__(self, user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': user_agent})
        self.rate_limit_delay = 2  # seconds between requests

    def generate_spam_sources(self, number: str) -> Dict[str, List[Tuple[str, str]]]:
        """
        Generate comprehensive spam check sources
        
        Args:
            number: Phone number to check
            
        Returns:
            Dictionary of spam source categories with lists of (name, url) tuples
        """
        # Clean number for different formats
        clean_number = number.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        international_number = number if number.startswith('+') else f'+{number}'
        
        categories = {
            "International Spam Databases": [
                ("Tellows", f"https://www.tellows.com/search?num={clean_number}"),
                ("Should I Answer", f"https://www.shouldianswer.com/phone-number/{clean_number}"),
                ("WhoCallsMe", f"https://whocallsme.com/Phone-Number.aspx/{clean_number}"),
                ("NumberGuru", f"https://www.numberguru.com/phone/{clean_number}"),
                ("SpamCalls", f"https://spamcalls.net/en/search?q={clean_number}"),
                ("TrueCaller", f"https://www.truecaller.com/search/{clean_number}"),
                ("SyncMe", f"https://sync.me/search/?number={clean_number}"),
                ("EveryCaller", f"https://everycaller.com/phone-number/{clean_number}"),
                ("CallerCenter", f"https://callercenter.com/{clean_number}"),
                ("PhoneHistory", f"https://www.phonehistory.com/{clean_number}")
            ],
            
            "Regional Spam Databases": [
                ("US: FTC Do Not Call", "https://www.donotcall.gov/"),
                ("US: FCC Complaints", "https://consumercomplaints.fcc.gov/hc/en-us"),
                ("UK: Ofcom", "https://www.ofcom.org.uk/"),
                ("India: TRAI DND", "https://www.trai.gov.in/"),
                ("Canada: National DNC", "https://lnnte-dncl.gc.ca/"),
                ("Australia: ACMA", "https://www.acma.gov.au/"),
                ("EU: Data Protection", "https://edpb.europa.eu/"),
                ("Germany: Tellows DE", f"https://www.tellows.de/num/{clean_number}"),
                ("France: Tellows FR", f"https://www.tellows.fr/num/{clean_number}"),
                ("Italy: Tellows IT", f"https://www.tellows.it/num/{clean_number}")
            ],
            
            "Search Engine Spam Reports": [
                ("Google Search", f"https://www.google.com/search?q=%22{clean_number}%22+spam+report"),
                ("Google Scam", f"https://www.google.com/search?q=%22{clean_number}%22+scam"),
                ("Google Fraud", f"https://www.google.com/search?q=%22{clean_number}%22+fraud"),
                ("Bing Search", f"https://www.bing.com/search?q=%22{clean_number}%22+spam"),
                ("DuckDuckGo", f"https://duckduckgo.com/?q=%22{clean_number}%22+spam"),
                ("Reddit Search", f"https://www.reddit.com/search/?q=%22{clean_number}%22"),
                ("Twitter Search", f"https://twitter.com/search?q=%22{clean_number}%22")
            ],
            
            "Business & Carrier Reports": [
                ("AT&T Call Protect", "https://www.att.com/callprotect/"),
                ("Verizon Call Filter", "https://www.verizon.com/call-filter/"),
                ("T-Mobile Scam Shield", "https://www.t-mobile.com/scamshield"),
                ("Sprint Call Screener", "https://www.sprint.com/en/landings/call-screener/"),
                ("Better Business Bureau", "https://www.bbb.org/"),
                ("FTC Scam Alerts", "https://www.consumer.ftc.gov/features/scam-alerts"),
                ("FCC Robocall Response", "https://www.fcc.gov/robocalls")
            ],
            
            "Community & Forum Reports": [
                ("800Notes", f"https://800notes.com/phone.aspx/{clean_number}"),
                ("CellRevealer", f"https://www.cellrevealer.com/{clean_number}"),
                ("SpamLok", f"https://spamlok.com/search/{clean_number}"),
                ("NumberCheck", f"https://www.numbercheck.com/number/{clean_number}"),
                ("PhoneNumberMonitor", f"https://www.phonenumbermonitor.com/search/{clean_number}"),
                ("ScamPhoneNumbers", f"https://www.scamphonenumbers.com/search/{clean_number}"),
                ("BadNumber", f"https://badnumber.com/number/{clean_number}"),
                ("KillerCalls", f"https://killercalls.com/phone/{clean_number}")
            ]
        }
        
        return categories

    def check_local_spam_patterns(self, number: str) -> List[str]:
        """
        Analyze number for common spam patterns
        
        Args:
            number: Phone number to analyze
            
        Returns:
            List of detected patterns
        """
        patterns = []
        clean_number = re.sub(r'[^\d+]', '', number)
        
        # Common spam number patterns
        spam_patterns = [
            (r'^\+?1?(\d{3})\1{2,}\d{4}$', 'Repeating digits pattern'),
            (r'^\+?1?(800|888|877|866|855|844|833)\d{7}$', 'Toll-free number'),
            (r'^\+?1?(900)\d{7}$', 'Premium rate number'),
            (r'^\+?1?(\d{3})000\d{4}$', 'Sequential zeros pattern'),
            (r'^\+?1?(\d{3})111\d{4}$', 'Sequential ones pattern'),
            (r'^\+?1?(\d{3})123\d{4}$', 'Sequential digits pattern'),
            (r'^\+?1?(\d{3})555\d{4}$', 'Common TV/Movie pattern'),
            (r'^\+?1?(\d{3})(\d{3})\2$', 'Repeated ending pattern')
        ]
        
        for pattern, description in spam_patterns:
            if re.match(pattern, clean_number):
                patterns.append(description)
        
        # Area code analysis
        suspicious_area_codes = [
            '268', '284', '664', '649', '767', '809', '829', '849',  # Caribbean premium
            '876', '868', '284', '340', '670', '671', '684', '787',  # Caribbean
            '900', '976'  # Premium rate
        ]
        
        area_code = clean_number[-10:-7] if len(clean_number) >= 10 else None
        if area_code in suspicious_area_codes:
            patterns.append(f"Suspicious area code: {area_code}")
        
        return patterns

    def generate_spam_search_terms(self, number: str) -> List[Tuple[str, str]]:
        """
        Generate comprehensive spam search terms
        
        Args:
            number: Phone number to check
            
        Returns:
            List of (search_type, search_url) tuples
        """
        clean_number = number.replace('+', '').replace(' ', '')
        
        search_terms = [
            ("Basic Spam Report", f"\"{clean_number}\" spam"),
            ("Scam Reports", f"\"{clean_number}\" scam"),
            ("Fraud Reports", f"\"{clean_number}\" fraud"),
            ("Robocall Reports", f"\"{clean_number}\" robocall"),
            ("Telemarketer", f"\"{clean_number}\" telemarketer"),
            ("Phishing", f"\"{clean_number}\" phishing"),
            ("Spoofing", f"\"{clean_number}\" spoofing"),
            ("Complaints", f"\"{clean_number}\" complaints"),
            ("Reviews", f"\"{clean_number}\" reviews"),
            ("Blacklist", f"\"{clean_number}\" blacklist"),
            ("Block", f"\"{clean_number}\" block"),
            ("Warning", f"\"{clean_number}\" warning"),
            ("Danger", f"\"{clean_number}\" dangerous"),
            ("Harassment", f"\"{clean_number}\" harassment"),
            ("Threat", f"\"{clean_number}\" threat")
        ]
        
        # Generate search URLs
        search_urls = []
        for term_type, search_term in search_terms:
            encoded_term = urllib.parse.quote(search_term)
            google_url = f"https://www.google.com/search?q={encoded_term}"
            bing_url = f"https://www.bing.com/search?q={encoded_term}"
            duckduckgo_url = f"https://duckduckgo.com/?q={encoded_term}"
            
            search_urls.extend([
                (f"Google - {term_type}", google_url),
                (f"Bing - {term_type}", bing_url),
                (f"DuckDuckGo - {term_type}", duckduckgo_url)
            ])
        
        return search_urls

    def display_spam_sources(self, number: str, spam_sources: Dict[str, List[Tuple[str, str]]]) -> None:
        """
        Display formatted spam check sources
        
        Args:
            number: Phone number being checked
            spam_sources: Dictionary of spam sources
        """
        print(Fore.RED + f"\n{'='*80}")
        print(Fore.RED + f"🚫 SPAM & SCAM REPORT CHECK FOR: {number}")
        print(Fore.RED + f"{'='*80}")
        
        total_sources = sum(len(sources) for sources in spam_sources.values())
        print(Fore.YELLOW + f"[📊] Total spam check sources: {total_sources}")
        
        for category, sources in spam_sources.items():
            print(Fore.CYAN + f"\n┌─ {category}")
            print(Fore.CYAN + f"├─ Sources: {len(sources)}")
            
            for i, (source_name, url) in enumerate(sources[:5], 1):  # Show first 5 per category
                print(Fore.GREEN + f"│  {i}. {source_name}")
                print(Fore.WHITE + f"│     {url}")
            
            if len(sources) > 5:
                print(Fore.YELLOW + f"│     ... and {len(sources) - 5} more sources")
            
            print(Fore.CYAN + "└─" + "─" * 50)

    def display_spam_patterns(self, number: str, patterns: List[str]) -> None:
        """
        Display detected spam patterns
        
        Args:
            number: Phone number analyzed
            patterns: List of detected patterns
        """
        if patterns:
            print(Fore.RED + f"\n[⚠️] DETECTED SPAM PATTERNS FOR {number}:")
            for pattern in patterns:
                print(Fore.RED + f"  • {pattern}")
        else:
            print(Fore.GREEN + f"\n[✅] No obvious spam patterns detected in {number}")

    def display_search_terms(self, search_terms: List[Tuple[str, str]]) -> None:
        """
        Display generated search terms
        
        Args:
            search_terms: List of search terms and URLs
        """
        print(Fore.YELLOW + f"\n[🔍] GENERATED SPAM SEARCH TERMS:")
        
        # Group by search engine
        search_engines = {}
        for term_name, url in search_terms:
            engine = term_name.split(' - ')[0]
            if engine not in search_engines:
                search_engines[engine] = []
            search_engines[engine].append((term_name, url))
        
        for engine, terms in search_engines.items():
            print(Fore.MAGENTA + f"\n  {engine}:")
            for term_name, url in terms[:3]:  # Show first 3 per engine
                search_type = term_name.split(' - ')[1]
                print(Fore.GREEN + f"    • {search_type}")
                print(Fore.WHITE + f"      {url}")

    def save_spam_report(self, number: str, spam_sources: Dict, patterns: List[str], 
                        search_terms: List[Tuple[str, str]], filename: str = None) -> None:
        """
        Save comprehensive spam report to file
        
        Args:
            number: Phone number checked
            spam_sources: Dictionary of spam sources
            patterns: List of detected patterns
            search_terms: List of search terms
            filename: Output filename
        """
        if filename is None:
            filename = f"spam_report_{number.replace('+', '')}.txt"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"SPAM & SCAM REPORT\n")
                f.write(f"Phone Number: {number}\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # Write patterns
                f.write("DETECTED PATTERNS:\n")
                if patterns:
                    for pattern in patterns:
                        f.write(f"• {pattern}\n")
                else:
                    f.write("• No obvious spam patterns detected\n")
                f.write("\n")
                
                # Write spam sources
                f.write("SPAM CHECK SOURCES:\n")
                f.write("-" * 40 + "\n")
                for category, sources in spam_sources.items():
                    f.write(f"\n{category}:\n")
                    for source_name, url in sources:
                        f.write(f"  • {source_name}: {url}\n")
                
                # Write search terms
                f.write("\n\nSEARCH TERMS:\n")
                f.write("-" * 40 + "\n")
                for term_name, url in search_terms:
                    f.write(f"  • {term_name}: {url}\n")
                
                # Legal disclaimer
                f.write("\n\nLEGAL DISCLAIMER:\n")
                f.write("This report is for informational purposes only. Use the information responsibly.\n")
                f.write("Respect privacy laws and terms of service of the listed platforms.\n")
            
            print(Fore.GREEN + f"[💾] Spam report saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"[❌] Error saving spam report: {e}")

    def spam_check(self, number: str, save_report: bool = False, check_patterns: bool = True) -> Dict:
        """
        Comprehensive spam check function
        
        Args:
            number: Phone number to check
            save_report: Whether to save report to file
            check_patterns: Whether to analyze number patterns
            
        Returns:
            Dictionary with all generated data
        """
        print(Fore.RED + f"\n[🚫] Starting comprehensive spam check for: {number}")
        
        # Generate spam sources
        spam_sources = self.generate_spam_sources(number)
        
        # Check for spam patterns
        patterns = []
        if check_patterns:
            patterns = self.check_local_spam_patterns(number)
        
        # Generate search terms
        search_terms = self.generate_spam_search_terms(number)
        
        # Display results
        self.display_spam_sources(number, spam_sources)
        
        if check_patterns:
            self.display_spam_patterns(number, patterns)
        
        self.display_search_terms(search_terms)
        
        # Save report if requested
        if save_report:
            self.save_spam_report(number, spam_sources, patterns, search_terms)
        
        # Legal disclaimer
        print(Fore.RED + "\n" + "="*80)
        print(Fore.RED + "[!] LEGAL DISCLAIMER:")
        print(Fore.RED + "    This tool aggregates publicly available spam reporting sources.")
        print(Fore.RED + "    Use this information responsibly and respect privacy laws.")
        print(Fore.RED + "    Always verify information from multiple sources.")
        
        return {
            'sources': spam_sources,
            'patterns': patterns,
            'search_terms': search_terms
        }

    def batch_spam_check(self, numbers: List[str], delay: float = 3.0) -> None:
        """
        Perform spam check on multiple numbers
        
        Args:
            numbers: List of phone numbers to check
            delay: Delay between checks in seconds
        """
        print(Fore.RED + f"\n[🚫] Starting batch spam check for {len(numbers)} numbers...")
        
        for i, number in enumerate(numbers, 1):
            print(Fore.YELLOW + f"\n[{i}/{len(numbers)}] Checking: {number}")
            self.spam_check(number)
            
            if i < len(numbers):  # No delay after last check
                print(Fore.YELLOW + f"[⏳] Waiting {delay} seconds...")
                time.sleep(delay)


# Simplified function for basic usage (backward compatibility)
def spam_check(number: str) -> None:
    """
    Simplified spam check function (backward compatible)
    
    Args:
        number: Phone number to check
    """
    checker = AdvancedSpamChecker()
    
    print(Fore.RED + f"\n[🚫] Spam Report Lookup for: {number}")
    
    # Original sources (maintaining backward compatibility)
    spam_sources = [
        ("Google Search", f"https://www.google.com/search?q=spam+report+{number}"),
        ("Tellows", f"https://www.tellows.com/search?num={number}"),
        ("Should I Answer", f"https://www.shouldianswer.com/phone-number/{number.replace('+', '')}")
    ]
    
    for source_name, url in spam_sources:
        print(Fore.GREEN + f"[Link] {source_name}: {url}")


# Example usage and testing
if __name__ == "__main__":
    # Create spam checker instance
    spam_checker = AdvancedSpamChecker()
    
    # Advanced usage
    report = spam_checker.spam_check("+919876543210", save_report=True, check_patterns=True)
    
    # Batch check
    numbers = ["+919876543210", "+11234567890", "+441234567890"]
    spam_checker.batch_spam_check(numbers, delay=5.0)
    
    # Or use simplified function (backward compatible)
    spam_check("+919876543210")