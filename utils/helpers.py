#!/usr/bin/env python3
"""
Utility Helpers
Description: Common utility functions for NumIntense
Version: 3.1.0
"""

import os
import sys
import time
from datetime import datetime
from colorama import Fore, Style

def check_platform():
    """Check and return platform information"""
    import platform
    system = platform.system().lower()
    architecture = platform.architecture()[0]
    return system, architecture

def create_report_directory():
    """Create reports directory if it doesn't exist"""
    if not os.path.exists('reports'):
        os.makedirs('reports')
    return 'reports'

def generate_filename(prefix, extension="txt"):
    """Generate timestamped filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"reports/{prefix}_{timestamp}.{extension}"

def print_legal_warning():
    """Print legal disclaimer"""
    print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  LEGAL DISCLAIMER")
    print(Fore.RED + "─" * 50)
    print(f"{Fore.YELLOW}• For authorized security research only")
    print(f"{Fore.YELLOW}• Comply with all applicable laws")
    print(f"{Fore.YELLOW}• Respect privacy and obtain authorization")
    print(f"{Fore.YELLOW}• Developers not liable for misuse")

def check_dependencies():
    """Check if required packages are installed"""
    required = ['phonenumbers', 'requests', 'colorama']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
            
    return missing

def format_phone_number(number):
    """Clean and format phone number"""
    import re
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', number)
    
    # Add country code if missing
    if not cleaned.startswith('+'):
        cleaned = '+91' + cleaned  # Default to India
        
    return cleaned

def is_valid_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_domain(domain):
    """Validate domain format"""
    import re
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
    return re.match(pattern, domain) is not None

class ProgressBar:
    """Simple progress bar for operations"""
    
    def __init__(self, total, prefix='Progress:', length=50):
        self.total = total
        self.prefix = prefix
        self.length = length
        self.current = 0
        
    def update(self, step=1):
        """Update progress bar"""
        self.current += step
        percent = (self.current / self.total) * 100
        filled = int(self.length * self.current // self.total)
        bar = '█' * filled + '░' * (self.length - filled)
        print(f'\r{Fore.CYAN}{self.prefix} |{bar}| {percent:.1f}%', end='', flush=True)
        
    def finish(self):
        """Complete progress bar"""
        print(f'\r{Fore.GREEN}{self.prefix} |{"█" * self.length}| 100.0% Complete!')