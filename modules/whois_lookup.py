# modules/whois_lookup.py

import whois
from colorama import Fore, Style, init
from typing import Dict, List, Optional
import json
import time
from datetime import datetime
import re

# Initialize colorama
init(autoreset=True)

class AdvancedWHOISLookup:
    def __init__(self, timeout: int = 10, retries: int = 2):
        self.timeout = timeout
        self.retries = retries
        self.results = {}

    def validate_domain(self, domain: str) -> bool:
        """
        Validate domain format
        
        Args:
            domain: Domain to validate
            
        Returns:
            Boolean indicating if domain is valid
        """
        # Basic domain pattern validation
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
        
        # Remove protocol if present
        domain = domain.lower().replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
        
        if re.match(domain_pattern, domain):
            return True
        else:
            print(Fore.RED + f"[❌] Invalid domain format: {domain}")
            return False

    def clean_domain(self, domain: str) -> str:
        """
        Clean and standardize domain input
        
        Args:
            domain: Raw domain input
            
        Returns:
            Cleaned domain string
        """
        domain = domain.strip().lower()
        
        # Remove common prefixes
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        
        # Remove path and query parameters
        domain = domain.split('/')[0]
        domain = domain.split('?')[0]
        
        return domain

    def perform_whois_lookup(self, domain: str) -> Optional[Dict]:
        """
        Perform WHOIS lookup with error handling and retries
        
        Args:
            domain: Domain to lookup
            
        Returns:
            WHOIS data dictionary or None if error
        """
        for attempt in range(self.retries):
            try:
                print(Fore.YELLOW + f"[🔄] WHOIS lookup attempt {attempt + 1}/{self.retries}...")
                
                result = whois.whois(domain)
                
                # Check if we got valid data
                if result and (result.domain_name or result.registrar):
                    return result
                else:
                    print(Fore.YELLOW + f"[⚠️] Attempt {attempt + 1} returned incomplete data")
                    
            except whois.parser.PywhoisError as e:
                if "No match" in str(e):
                    print(Fore.RED + f"[❌] Domain not found in WHOIS database: {domain}")
                    return None
                else:
                    print(Fore.RED + f"[❌] WHOIS parser error (attempt {attempt + 1}): {e}")
                    
            except Exception as e:
                print(Fore.RED + f"[❌] Unexpected error (attempt {attempt + 1}): {e}")
            
            # Wait before retry
            if attempt < self.retries - 1:
                time.sleep(2)
        
        return None

    def format_whois_data(self, whois_data: Dict) -> Dict[str, any]:
        """
        Format and extract WHOIS data in a structured way
        
        Args:
            whois_data: Raw WHOIS data
            
        Returns:
            Structured WHOIS information
        """
        formatted = {}
        
        try:
            # Basic domain information
            formatted['domain_name'] = self._safe_get(whois_data, 'domain_name')
            formatted['registrar'] = self._safe_get(whois_data, 'registrar')
            formatted['whois_server'] = self._safe_get(whois_data, 'whois_server')
            
            # Dates
            formatted['creation_date'] = self._format_date(self._safe_get(whois_data, 'creation_date'))
            formatted['expiration_date'] = self._format_date(self._safe_get(whois_data, 'expiration_date'))
            formatted['updated_date'] = self._format_date(self._safe_get(whois_data, 'updated_date'))
            
            # Registrant information
            formatted['registrant_name'] = self._safe_get(whois_data, 'name')
            formatted['registrant_organization'] = self._safe_get(whois_data, 'org')
            formatted['registrant_country'] = self._safe_get(whois_data, 'country')
            formatted['registrant_email'] = self._safe_get(whois_data, 'emails')
            
            # Technical information
            formatted['name_servers'] = self._safe_get(whois_data, 'name_servers')
            formatted['status'] = self._safe_get(whois_data, 'status')
            formatted['dnssec'] = self._safe_get(whois_data, 'dnssec')
            
            # Additional metadata
            formatted['raw_data'] = str(whois_data)
            formatted['lookup_timestamp'] = datetime.now().isoformat()
            
        except Exception as e:
            print(Fore.RED + f"[❌] Error formatting WHOIS data: {e}")
            formatted['error'] = str(e)
        
        return formatted

    def _safe_get(self, data: Dict, key: str, default: any = "Not Available") -> any:
        """
        Safely get value from WHOIS data with handling for multiple formats
        
        Args:
            data: WHOIS data dictionary
            key: Key to retrieve
            default: Default value if not found
            
        Returns:
            Value or default
        """
        try:
            value = getattr(data, key, default)
            
            # Handle cases where value might be a list
            if isinstance(value, list) and value:
                return value[0] if len(value) == 1 else value
            elif value is None or value == []:
                return default
            else:
                return value
                
        except Exception:
            return default

    def _format_date(self, date_value) -> str:
        """
        Format date values consistently
        
        Args:
            date_value: Raw date value
            
        Returns:
            Formatted date string
        """
        if not date_value or date_value == "Not Available":
            return "Not Available"
        
        try:
            if isinstance(date_value, list):
                date_value = date_value[0]
            
            if isinstance(date_value, str):
                return date_value
            else:
                return date_value.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return "Invalid Date"

    def calculate_domain_age(self, creation_date: str) -> str:
        """
        Calculate domain age from creation date
        
        Args:
            creation_date: Domain creation date
            
        Returns:
            Formatted domain age string
        """
        if not creation_date or creation_date == "Not Available":
            return "Unknown"
        
        try:
            if isinstance(creation_date, str):
                # Try to parse string date
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d-%b-%Y"]:
                    try:
                        created = datetime.strptime(creation_date.split()[0], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return "Unknown"
            else:
                created = creation_date
            
            now = datetime.now()
            age_days = (now - created).days
            age_years = age_days // 365
            remaining_days = age_days % 365
            
            if age_years > 0:
                return f"{age_years} years, {remaining_days} days"
            else:
                return f"{age_days} days"
                
        except Exception:
            return "Unknown"

    def check_domain_expiry(self, expiration_date: str) -> Dict[str, str]:
        """
        Check domain expiry status
        
        Args:
            expiration_date: Domain expiration date
            
        Returns:
            Expiry status information
        """
        if not expiration_date or expiration_date == "Not Available":
            return {"status": "Unknown", "days_remaining": "N/A"}
        
        try:
            if isinstance(expiration_date, str):
                # Try to parse string date
                for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d-%b-%Y"]:
                    try:
                        expiry = datetime.strptime(expiration_date.split()[0], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return {"status": "Unknown", "days_remaining": "N/A"}
            else:
                expiry = expiration_date
            
            now = datetime.now()
            days_remaining = (expiry - now).days
            
            if days_remaining < 0:
                return {"status": "EXPIRED", "days_remaining": str(abs(days_remaining))}
            elif days_remaining < 30:
                return {"status": "CRITICAL", "days_remaining": str(days_remaining)}
            elif days_remaining < 90:
                return {"status": "WARNING", "days_remaining": str(days_remaining)}
            else:
                return {"status": "OK", "days_remaining": str(days_remaining)}
                
        except Exception:
            return {"status": "Unknown", "days_remaining": "N/A"}

    def display_whois_results(self, domain: str, whois_info: Dict) -> None:
        """
        Display formatted WHOIS results
        
        Args:
            domain: Original domain
            whois_info: Formatted WHOIS information
        """
        print(Fore.CYAN + f"\n{'='*80}")
        print(Fore.CYAN + f"🌐 WHOIS LOOKUP RESULTS FOR: {domain}")
        print(Fore.CYAN + f"{'='*80}")
        
        # Domain Age and Expiry
        domain_age = self.calculate_domain_age(whois_info.get('creation_date'))
        expiry_status = self.check_domain_expiry(whois_info.get('expiration_date'))
        
        print(Fore.YELLOW + f"\n[📊] DOMAIN METADATA:")
        print(Fore.WHITE + f"  🔹 Domain Age: {domain_age}")
        
        status_color = {
            'OK': Fore.GREEN,
            'WARNING': Fore.YELLOW,
            'CRITICAL': Fore.RED,
            'EXPIRED': Fore.RED,
            'Unknown': Fore.WHITE
        }.get(expiry_status['status'], Fore.WHITE)
        
        print(status_color + f"  🔹 Expiry Status: {expiry_status['status']} ({expiry_status['days_remaining']} days)")
        
        # Registrar Information
        print(Fore.YELLOW + f"\n[🏢] REGISTRAR INFORMATION:")
        print(Fore.WHITE + f"  🔹 Registrar: {whois_info.get('registrar')}")
        print(Fore.WHITE + f"  🔹 WHOIS Server: {whois_info.get('whois_server')}")
        
        # Date Information
        print(Fore.YELLOW + f"\n[📅] DATE INFORMATION:")
        print(Fore.WHITE + f"  🔹 Creation Date: {whois_info.get('creation_date')}")
        print(Fore.WHITE + f"  🔹 Expiration Date: {whois_info.get('expiration_date')}")
        print(Fore.WHITE + f"  🔹 Last Updated: {whois_info.get('updated_date')}")
        
        # Registrant Information
        print(Fore.YELLOW + f"\n[👤] REGISTRANT INFORMATION:")
        print(Fore.WHITE + f"  🔹 Name: {whois_info.get('registrant_name')}")
        print(Fore.WHITE + f"  🔹 Organization: {whois_info.get('registrant_organization')}")
        print(Fore.WHITE + f"  🔹 Country: {whois_info.get('registrant_country')}")
        
        # Email Information (with privacy protection check)
        emails = whois_info.get('registrant_email')
        if emails and emails != "Not Available":
            if any(privacy_indicator in str(emails).lower() for privacy_indicator in 
                  ['privacy', 'protected', 'redacted', 'whois', 'domain']):
                print(Fore.YELLOW + f"  🔹 Email: [PRIVACY PROTECTED]")
            else:
                print(Fore.WHITE + f"  🔹 Email: {emails}")
        
        # Technical Information
        print(Fore.YELLOW + f"\n[🔧] TECHNICAL INFORMATION:")
        
        # Name Servers
        name_servers = whois_info.get('name_servers')
        if name_servers and name_servers != "Not Available":
            print(Fore.WHITE + f"  🔹 Name Servers:")
            if isinstance(name_servers, list):
                for ns in name_servers[:3]:  # Show first 3
                    print(Fore.WHITE + f"     • {ns}")
                if len(name_servers) > 3:
                    print(Fore.YELLOW + f"     • ... and {len(name_servers) - 3} more")
            else:
                print(Fore.WHITE + f"     • {name_servers}")
        
        # Domain Status
        status = whois_info.get('status')
        if status and status != "Not Available":
            print(Fore.WHITE + f"  🔹 Status: {status}")
        
        # DNSSEC
        dnssec = whois_info.get('dnssec')
        if dnssec and dnssec != "Not Available":
            print(Fore.WHITE + f"  🔹 DNSSEC: {dnssec}")

    def save_whois_report(self, domain: str, whois_info: Dict, filename: str = None) -> None:
        """
        Save WHOIS report to file
        
        Args:
            domain: Domain name
            whois_info: WHOIS information
            filename: Output filename
        """
        if filename is None:
            filename = f"whois_report_{domain.replace('.', '_')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"WHOIS LOOKUP REPORT\n")
                f.write(f"Domain: {domain}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # Write structured data
                for category, value in whois_info.items():
                    if category != 'raw_data':  # Skip raw data in text report
                        f.write(f"{category.upper().replace('_', ' ')}: {value}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("END OF REPORT\n")
            
            print(Fore.GREEN + f"[💾] WHOIS report saved to: {filename}")
            
        except Exception as e:
            print(Fore.RED + f"[❌] Error saving WHOIS report: {e}")

    def whois_lookup(self, domain: str, save_report: bool = False) -> Optional[Dict]:
        """
        Main WHOIS lookup function
        
        Args:
            domain: Domain to lookup
            save_report: Whether to save report to file
            
        Returns:
            WHOIS information dictionary or None if error
        """
        print(Fore.BLUE + f"\n[🌐] Starting WHOIS lookup for: {domain}")
        
        # Clean and validate domain
        clean_domain = self.clean_domain(domain)
        
        if not self.validate_domain(clean_domain):
            return None
        
        print(Fore.YELLOW + f"[🔍] Looking up: {clean_domain}")
        
        # Perform WHOIS lookup
        whois_data = self.perform_whois_lookup(clean_domain)
        
        if not whois_data:
            print(Fore.RED + f"[❌] WHOIS lookup failed for: {clean_domain}")
            return None
        
        # Format and display results
        formatted_info = self.format_whois_data(whois_data)
        self.display_whois_results(clean_domain, formatted_info)
        
        # Save report if requested
        if save_report:
            self.save_whois_report(clean_domain, formatted_info)
        
        print(Fore.GREEN + f"\n[✅] WHOIS lookup completed for: {clean_domain}")
        
        return formatted_info

    def batch_whois_lookup(self, domains: List[str], delay: float = 3.0) -> Dict[str, Optional[Dict]]:
        """
        Perform WHOIS lookup on multiple domains
        
        Args:
            domains: List of domains to lookup
            delay: Delay between lookups in seconds
            
        Returns:
            Dictionary of domain -> WHOIS results
        """
        print(Fore.BLUE + f"\n[🌐] Starting batch WHOIS lookup for {len(domains)} domains...")
        
        results = {}
        
        for i, domain in enumerate(domains, 1):
            print(Fore.YELLOW + f"\n[{i}/{len(domains)}] Processing: {domain}")
            
            result = self.whois_lookup(domain)
            results[domain] = result
            
            if i < len(domains):  # No delay after last domain
                print(Fore.YELLOW + f"[⏳] Waiting {delay} seconds...")
                time.sleep(delay)
        
        successful = sum(1 for result in results.values() if result is not None)
        print(Fore.GREEN + f"\n[📊] Batch complete: {successful}/{len(domains)} successful lookups")
        
        return results


# Simplified function for basic usage (backward compatibility)
def whois_lookup(domain: str) -> None:
    """
    Simplified WHOIS lookup function (backward compatible)
    
    Args:
        domain: Domain to lookup
    """
    lookup = AdvancedWHOISLookup()
    
    print(Fore.BLUE + f"\n[🌐] WHOIS Lookup for: {domain}")
    
    try:
        result = whois.whois(domain)
        
        if result.domain_name:
            print(Fore.CYAN + f"🔹 Registrar: {result.registrar}")
            print(Fore.CYAN + f"🔹 Creation Date: {result.creation_date}")
            print(Fore.CYAN + f"🔹 Expiration Date: {result.expiration_date}")
            
            # Show first few name servers
            if result.name_servers:
                servers = list(result.name_servers)[:3]
                print(Fore.CYAN + f"🔹 Name Servers: {', '.join(servers)}")
                if len(result.name_servers) > 3:
                    print(Fore.CYAN + f"🔹 ... and {len(result.name_servers) - 3} more")
            
            if result.emails:
                print(Fore.CYAN + f"🔹 Emails: {result.emails}")
        else:
            print(Fore.YELLOW + "⚠️ No WHOIS data found.")
            
    except Exception as e:
        print(Fore.RED + f"[x] Error during WHOIS lookup: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Create WHOIS lookup instance
    whois_tool = AdvancedWHOISLookup()
    
    # Single domain lookup
    result = whois_tool.whois_lookup("google.com", save_report=True)
    
    # Batch lookup
    domains = ["github.com", "microsoft.com", "python.org"]
    batch_results = whois_tool.batch_whois_lookup(domains, delay=2.0)
    
    # Or use simplified function
    whois_lookup("wikipedia.org")