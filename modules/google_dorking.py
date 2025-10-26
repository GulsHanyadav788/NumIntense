import urllib.parse
from colorama import Fore, Style, init
from typing import List, Dict, Tuple
import re

# Initialize colorama
init(autoreset=True)

class AdvancedDorkGenerator:
    def __init__(self):
        self.search_engines = {
            "Google": "https://www.google.com/search?q={}",
            "DuckDuckGo": "https://duckduckgo.com/html/?q={}",
            "Bing": "https://www.bing.com/search?q={}",
            "Yandex": "https://yandex.com/search/?text={}",
            "Startpage": "https://www.startpage.com/sp/search?query={}",
            "Brave": "https://search.brave.com/search?q={}",
            "Qwant": "https://www.qwant.com/?q={}",
            "Ecosia": "https://www.ecosia.org/search?q={}"
        }

    def clean_number_variations(self, number: str) -> List[str]:
        """
        Generate multiple variations of the phone number
        
        Args:
            number: Original phone number
            
        Returns:
            List of number variations
        """
        variations = []
        
        # Original number
        variations.append(number)
        
        # Clean different formats
        clean_variations = [
            number.replace(' ', '').replace('-', '').replace('(', '').replace(')', ''),
            number.replace(' ', '-'),
            number.replace(' ', ''),
            number.replace('+', ''),
            re.sub(r'[^\d+]', '', number)
        ]
        
        variations.extend(clean_variations)
        
        # Country code specific variations
        if number.startswith('+91'):  # India
            variations.extend([
                number[3:],  # Without country code
                '0' + number[3:],  # With leading zero
                number.replace('+91', '91')  # Without plus
            ])
        elif number.startswith('+1'):  # US/Canada
            variations.extend([
                number[2:],  # Without country code
                number.replace('+1', '1')  # Without plus
            ])
        elif number.startswith('+44'):  # UK
            variations.extend([
                number[3:],  # Without country code
                '0' + number[3:],  # With leading zero
                number.replace('+44', '44')  # Without plus
            ])
        
        # Remove duplicates and empty strings
        variations = list(set([v for v in variations if v.strip()]))
        return variations

    def generate_social_media_dorks(self, number_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate social media specific dorks
        
        Args:
            number_variations: List of number formats
            
        Returns:
            List of (platform, dork_query) tuples
        """
        social_platforms = [
            ("Facebook", "site:facebook.com"),
            ("Instagram", "site:instagram.com"),
            ("Twitter", "site:twitter.com"),
            ("LinkedIn", "site:linkedin.com"),
            ("Pinterest", "site:pinterest.com"),
            ("Reddit", "site:reddit.com"),
            ("Telegram", "site:t.me OR site:telegram.me"),
            ("WhatsApp", "site:whatsapp.com OR site:wa.me"),
            ("Signal", "site:signal.org"),
            ("Viber", "site:viber.com"),
            ("WeChat", "site:wechat.com"),
            ("Snapchat", "site:snapchat.com"),
            ("TikTok", "site:tiktok.com"),
            ("YouTube", "site:youtube.com"),
            ("Discord", "site:discord.com"),
            ("Skype", "site:skype.com"),
            ("Line", "site:line.me"),
            ("Kik", "site:kik.com"),
            ("Clubhouse", "site:clubhouse.com")
        ]
        
        dorks = []
        for platform, site_filter in social_platforms:
            for num_var in number_variations[:3]:  # Use first 3 variations
                dorks.append((
                    f"{platform} - {num_var}",
                    f'intext:"{num_var}" {site_filter}'
                ))
        
        return dorks

    def generate_document_dorks(self, number_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate document and file type dorks
        
        Args:
            number_variations: List of number formats
            
        Returns:
            List of (file_type, dork_query) tuples
        """
        file_types = [
            ("PDF Documents", "ext:pdf"),
            ("Word Documents", "ext:doc OR ext:docx"),
            ("Excel Files", "ext:xls OR ext:xlsx"),
            ("Text Files", "ext:txt"),
            ("CSV Files", "ext:csv"),
            ("Presentations", "ext:ppt OR ext:pptx"),
            ("Images", "ext:jpg OR ext:jpeg OR ext:png OR ext:gif"),
            ("Archives", "ext:zip OR ext:rar OR ext:7z"),
            ("Database Files", "ext:sql OR ext:db OR ext:mdb")
        ]
        
        dorks = []
        for file_type, ext_filter in file_types:
            for num_var in number_variations[:2]:  # Use first 2 variations
                dorks.append((
                    f"{file_type} - {num_var}",
                    f'"{num_var}" {ext_filter}'
                ))
        
        return dorks

    def generate_pastebin_dorks(self, number_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate pastebin and code sharing site dorks
        
        Args:
            number_variations: List of number formats
            
        Returns:
            List of (site, dork_query) tuples
        """
        paste_sites = [
            ("Pastebin", "site:pastebin.com"),
            ("GitHub", "site:github.com"),
            ("GitLab", "site:gitlab.com"),
            ("Bitbucket", "site:bitbucket.org"),
            ("SourceForge", "site:sourceforge.net"),
            ("CodePen", "site:codepen.io"),
            ("JSFiddle", "site:jsfiddle.net"),
            ("Paste.org", "site:paste.org"),
            ("Paste.org.ru", "site:paste.org.ru"),
            ("Rentry", "site:rentry.co"),
            ("PrivateBin", "site:privatebin.net"),
            ("Hastebin", "site:hastebin.com"),
            ("Ghostbin", "site:ghostbin.com")
        ]
        
        dorks = []
        for site_name, site_filter in paste_sites:
            for num_var in number_variations[:3]:
                dorks.append((
                    f"{site_name} - {num_var}",
                    f'"{num_var}" {site_filter}'
                ))
        
        return dorks

    def generate_forum_dorks(self, number_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate forum and discussion board dorks
        
        Args:
            number_variations: List of number formats
            
        Returns:
            List of (forum_type, dork_query) tuples
        """
        forum_platforms = [
            ("phpBB Forums", "site:*.phpbb.com OR inurl:phpbb"),
            ("vBulletin Forums", "site:*.vbulletin.net OR inurl:vbulletin"),
            ("XenForo Forums", "site:*.xenforo.com OR inurl:xenforo"),
            ("Discourse Forums", "site:*.discourse.group"),
            ("Flarum Forums", "site:*.flarum.cloud"),
            ("Simple Machines", "site:*.simplemachines.org"),
            ("Quora", "site:quora.com"),
            ("Stack Overflow", "site:stackoverflow.com"),
            ("Reddit Threads", "site:reddit.com")
        ]
        
        dorks = []
        for forum_type, site_filter in forum_platforms:
            for num_var in number_variations[:2]:
                dorks.append((
                    f"{forum_type} - {num_var}",
                    f'"{num_var}" {site_filter}'
                ))
        
        return dorks

    def generate_business_dorks(self, number_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate business and professional dorks
        
        Args:
            number_variations: List of number formats
            
        Returns:
            List of (business_type, dork_query) tuples
        """
        business_sites = [
            ("Yellow Pages", "site:yellowpages.com OR site:yellowpages.ca"),
            ("White Pages", "site:whitepages.com OR site:whitepages.ca"),
            ("TrueCaller", "site:truecaller.com"),
            ("SpyDialer", "site:spydialer.com"),
            ("411", "site:411.com"),
            ("AnyWho", "site:anywho.com"),
            ("LinkedIn Profiles", "site:linkedin.com/in/ OR site:linkedin.com/pub/"),
            ("AngelList", "site:angel.co"),
            ("Crunchbase", "site:crunchbase.com"),
            ("Glassdoor", "site:glassdoor.com"),
            ("Indeed", "site:indeed.com"),
            ("Monster", "site:monster.com"),
            ("CareerBuilder", "site:careerbuilder.com")
        ]
        
        dorks = []
        for business_type, site_filter in business_sites:
            for num_var in number_variations[:2]:
                dorks.append((
                    f"{business_type} - {num_var}",
                    f'"{num_var}" {site_filter}'
                ))
        
        return dorks

    def generate_advanced_dorks(self, number_variations: List[str]) -> List[Tuple[str, str]]:
        """
        Generate advanced and combination dorks
        
        Args:
            number_variations: List of number formats
            
        Returns:
            List of (dork_type, dork_query) tuples
        """
        advanced_dorks = []
        
        for num_var in number_variations[:3]:
            advanced_dorks.extend([
                (
                    f"Contact Pages - {num_var}",
                    f'inurl:contact "{num_var}"'
                ),
                (
                    f"About Pages - {num_var}",
                    f'inurl:about "{num_var}"'
                ),
                (
                    f"Profile Pages - {num_var}",
                    f'inurl:profile "{num_var}"'
                ),
                (
                    f"Phone Directory - {num_var}",
                    f'inurl:phone "{num_var}" OR inurl:telephone "{num_var}"'
                ),
                (
                    f"User Profiles - {num_var}",
                    f'inurl:user "{num_var}" OR inurl:users "{num_var}"'
                ),
                (
                    f"Member Directory - {num_var}",
                    f'inurl:members "{num_var}" OR inurl:directory "{num_var}"'
                ),
                (
                    f"Excel/CSV Files - {num_var}",
                    f'"{num_var}" (ext:xls OR ext:xlsx OR ext:csv)'
                ),
                (
                    f"Database Dumps - {num_var}",
                    f'"{num_var}" (ext:sql OR ext:db OR ext:bak)'
                ),
                (
                    f"Config Files - {num_var}",
                    f'"{num_var}" (ext:config OR ext:conf OR ext:ini)'
                ),
                (
                    f"Log Files - {num_var}",
                    f'"{num_var}" (ext:log OR ext:txt)'
                )
            ])
        
        return advanced_dorks

    def generate_all_dorks(self, number: str) -> Dict[str, List[Tuple[str, str]]]:
        """
        Generate all types of dorks for a phone number
        
        Args:
            number: Phone number to generate dorks for
            
        Returns:
            Dictionary of dork categories with lists of (name, query) tuples
        """
        number_variations = self.clean_number_variations(number)
        
        return {
            "Social Media": self.generate_social_media_dorks(number_variations),
            "Documents": self.generate_document_dorks(number_variations),
            "Paste Sites": self.generate_pastebin_dorks(number_variations),
            "Forums": self.generate_forum_dorks(number_variations),
            "Business": self.generate_business_dorks(number_variations),
            "Advanced": self.generate_advanced_dorks(number_variations)
        }

    def generate_search_urls(self, dorks: Dict[str, List[Tuple[str, str]]]) -> Dict[str, Dict[str, List[Tuple[str, str]]]]:
        """
        Generate search URLs for all dorks across all search engines
        
        Args:
            dorks: Dictionary of dork categories
            
        Returns:
            Nested dictionary: engine -> category -> list of (name, url)
        """
        search_results = {}
        
        for engine, base_url in self.search_engines.items():
            engine_results = {}
            
            for category, dork_list in dorks.items():
                category_urls = []
                
                for dork_name, dork_query in dork_list:
                    encoded_query = urllib.parse.quote(dork_query)
                    url = base_url.format(encoded_query)
                    category_urls.append((dork_name, url))
                
                engine_results[category] = category_urls
            
            search_results[engine] = engine_results
        
        return search_results

    def display_dorks(self, number: str, search_urls: Dict[str, Dict[str, List[Tuple[str, str]]]]) -> None:
        """
        Display generated dorks in a formatted way
        
        Args:
            number: Original phone number
            search_urls: Generated search URLs
        """
        print(Fore.CYAN + f"\n{'='*80}")
        print(Fore.CYAN + f"🎯 ADVANCED DORK GENERATION FOR: {number}")
        print(Fore.CYAN + f"{'='*80}")
        
        for engine, categories in search_urls.items():
            print(Fore.YELLOW + f"\n┌─ {engine} Search Engine")
            
            total_dorks = sum(len(dorks) for dorks in categories.values())
            print(Fore.YELLOW + f"├─ Total Dorks: {total_dorks}")
            
            for category, dorks in categories.items():
                print(Fore.MAGENTA + f"├─ {category} ({len(dorks)} dorks)")
                
                # Show first 2 dorks per category as examples
                for i, (dork_name, url) in enumerate(dorks[:2]):
                    print(Fore.GREEN + f"│  {i+1}. {dork_name}")
                    print(Fore.WHITE + f"│     {url}")
                
                if len(dorks) > 2:
                    print(Fore.CYAN + f"│     ... and {len(dorks) - 2} more")
            
            print(Fore.YELLOW + "└─" + "─" * 50)

    def save_dorks_to_file(self, number: str, search_urls: Dict, filename: str = None) -> None:
        """
        Save all generated dorks to a text file
        
        Args:
            number: Phone number searched
            search_urls: Generated search URLs
            filename: Output filename
        """
        if filename is None:
            filename = f"dorks_{number.replace('+', '')}.txt"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Advanced Dork Generation Report\n")
                f.write(f"Phone Number: {number}\n")
                f.write("=" * 60 + "\n\n")
                
                for engine, categories in search_urls.items():
                    f.write(f"{engine} SEARCH ENGINE:\n")
                    f.write("-" * 40 + "\n")
                    
                    for category, dorks in categories.items():
                        f.write(f"\n{category}:\n")
                        for dork_name, url in dorks:
                            f.write(f"  • {dork_name}\n")
                            f.write(f"    {url}\n")
                            f.write(f"\n")
                    f.write("\n" + "="*60 + "\n\n")
            
            print(Fore.GREEN + f"[💾] Dorks saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"[❌] Error saving dorks: {e}")

    def generate_dorks(self, number: str, save_output: bool = False, max_dorks_per_category: int = 5) -> Dict:
        """
        Main function to generate comprehensive dorks
        
        Args:
            number: Phone number to investigate
            save_output: Whether to save results to file
            max_dorks_per_category: Limit dorks per category
            
        Returns:
            Dictionary with generated search URLs
        """
        print(Fore.CYAN + f"\n[🎯] Generating advanced dorks for: {number}")
        
        # Generate all dork types
        all_dorks = self.generate_all_dorks(number)
        
        # Limit dorks per category if specified
        if max_dorks_per_category:
            for category in all_dorks:
                all_dorks[category] = all_dorks[category][:max_dorks_per_category]
        
        # Generate search URLs
        search_urls = self.generate_search_urls(all_dorks)
        
        # Display results
        self.display_dorks(number, search_urls)
        
        # Save to file if requested
        if save_output:
            self.save_dorks_to_file(number, search_urls)
        
        print(Fore.RED + "\n[!] LEGAL DISCLAIMER: Use these dorks responsibly and ethically.")
        print(Fore.RED + "    Respect robots.txt, terms of service, and applicable laws.")
        
        return search_urls


# Simplified function for basic usage (backward compatibility)
def generate_dorks(number: str) -> List[str]:
    """
    Simplified dork generation (backward compatible with original function)
    
    Args:
        number: Phone number
        
    Returns:
        List of Google search URLs
    """
    generator = AdvancedDorkGenerator()
    basic_dorks = [
        f'intext:"{number}" site:facebook.com',
        f'intext:"{number}" site:instagram.com',
        f'intext:"{number}" site:linkedin.com',
        f'intext:"{number}" site:twitter.com',
        f'intext:"{number}" site:pinterest.com',
        f'intext:"{number}" site:pastebin.com',
        f'intext:"{number}" ext:pdf OR ext:doc',
        f'"{number}"'
    ]
    
    return [f"https://www.google.com/search?q={urllib.parse.quote(dork)}" for dork in basic_dorks]


# Example usage and testing
if __name__ == "__main__":
    # Create generator instance
    dork_gen = AdvancedDorkGenerator()
    
    # Advanced usage
    search_results = dork_gen.generate_dorks("+919876543210", save_output=True, max_dorks_per_category=3)
    
    # Or use simplified function (backward compatible)
    basic_dorks = generate_dorks("+919876543210")
    print(f"\nBasic dorks generated: {len(basic_dorks)}")