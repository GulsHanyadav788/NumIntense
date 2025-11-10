#!/usr/bin/env python3
"""
NumIntense - Installation System
Description: Automated deployment for OSINT Intelligence Suite
Version: 3.1.0
Author: GulsHan Kumar
"""

import sys
import subprocess
import os
import platform
import time
from datetime import datetime
from colorama import init, Fore, Style
import random

init(autoreset=True)

class NumIntenseInstaller:
    def __init__(self):
        self.start_time = datetime.now()
        self.platform = platform.system().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.install_id = self.generate_install_id()

    def generate_install_id(self):
        """Generate unique installation ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        return f"INSTALL-{timestamp}-{random_id}"

    def print_banner(self):
        """Display professional banner"""
        print(Fore.MAGENTA + Style.BRIGHT + """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    ███╗   ██╗██╗   ██╗███╗   ███╗██╗███╗   ██╗████████╗███████╗███╗   ██╗███████╗    ║
    ║    ████╗  ██║██║   ██║████╗ ████║██║████╗  ██║╚══██╔══╝██╔════╝████╗  ██║██╔════╝    ║
    ║    ██╔██╗ ██║██║   ██║██╔████╔██║██║██╔██╗ ██║   ██║   █████╗  ██╔██╗ ██║█████╗      ║
    ║    ██║╚██╗██║██║   ██║██║╚██╔╝██║██║██║╚██╗██║   ██║   ██╔══╝  ██║╚██╗██║██╔══╝      ║
    ║    ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║   ██║   ███████╗██║ ╚████║███████╗    ║
    ║    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝    ║
    ║                                                                              ║
    ║                    🔥 ULTIMATE OSINT INTELLIGENCE SUITE                     ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        print(Fore.CYAN + Style.BRIGHT + "    " + "═" * 70)
        print(Fore.YELLOW + f"    🚀 Version 3.1.0 | Enterprise Edition | Install ID: {self.install_id}")
        print(Fore.GREEN + f"    📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.GREEN + f"    🖥️  Platform: {self.platform.title()} | Python: {self.python_version}")
        print(Fore.CYAN + "    " + "═" * 70)
        print()

    def print_status(self, step, message, status="INFO"):
        status_config = {
            "SUCCESS": {"color": Fore.GREEN, "icon": "✅"},
            "ERROR": {"color": Fore.RED, "icon": "❌"},
            "WARNING": {"color": Fore.YELLOW, "icon": "⚠️"},
            "INFO": {"color": Fore.CYAN, "icon": "🔹"},
            "PROCESSING": {"color": Fore.BLUE, "icon": "🔄"}
        }
        config = status_config.get(status, status_config["INFO"])
        print(f"{config['color']}{config['icon']} [{step}] {message}")

    def check_python(self):
        self.print_status("PYTHON", "Checking Python version...", "PROCESSING")
        if sys.version_info < (3, 6):
            self.print_status("PYTHON", "Python 3.6+ required", "ERROR")
            return False
        self.print_status("PYTHON", f"Version {self.python_version} OK", "SUCCESS")
        return True

    def check_platform(self):
        self.print_status("SYSTEM", "Checking platform...", "PROCESSING")
        supported = ['linux', 'darwin', 'windows']
        if self.platform not in supported:
            self.print_status("SYSTEM", f"Unsupported: {self.platform}", "WARNING")
        else:
            self.print_status("SYSTEM", f"{self.platform.title()} supported", "SUCCESS")
        return True

    def check_file_structure(self):
        """Check if essential files exist"""
        self.print_status("SETUP", "Verifying file structure...", "PROCESSING")
        
        essential_files = [
            "numintense_pro.py",
            "requirements.txt", 
            "config.json",
            "README.md"
        ]
        
        missing_files = []
        
        for file in essential_files:
            if os.path.exists(file):
                self.print_status("FILE", f"Found: {file}", "SUCCESS")
            else:
                missing_files.append(file)
                self.print_status("FILE", f"Missing: {file}", "WARNING")
        
        if missing_files:
            self.print_status("SETUP", f"Missing files: {', '.join(missing_files)}", "WARNING")
            return False
        
        self.print_status("SETUP", "All essential files verified", "SUCCESS")
        return True

    def upgrade_pip(self):
        self.print_status("PIP", "Upgrading pip...", "PROCESSING")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         capture_output=True, timeout=60)
            self.print_status("PIP", "Pip upgraded", "SUCCESS")
        except:
            self.print_status("PIP", "Pip upgrade skipped", "WARNING")

    def install_requirements(self):
        self.print_status("DEPS", "Installing dependencies...", "PROCESSING")
        try:
            if os.path.exists("requirements.txt"):
                process = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
                ], capture_output=True, text=True)
                
                if process.returncode == 0:
                    self.print_status("DEPS", "Dependencies installed", "SUCCESS")
                    return True
                else:
                    self.print_status("DEPS", "Installation had issues", "WARNING")
                    return True
            else:
                self.print_status("DEPS", "requirements.txt not found", "ERROR")
                return False
        except Exception as e:
            self.print_status("DEPS", f"Error: {e}", "ERROR")
            return False

    def verify_installation(self):
        self.print_status("VERIFY", "Verifying installation...", "PROCESSING")
        packages = {
            "phonenumbers": "Phone number processing",
            "requests": "HTTP requests", 
            "colorama": "Terminal colors",
            "whois": "Domain lookup"
        }
        
        for pkg, desc in packages.items():
            try:
                __import__(pkg)
                self.print_status("VERIFY", f"{pkg}: {desc}", "SUCCESS")
            except ImportError:
                self.print_status("VERIFY", f"{pkg}: MISSING", "ERROR")
                return False
        return True

    def create_dirs(self):
        self.print_status("SETUP", "Creating directories...", "PROCESSING")
        dirs = ["reports", "data", "logs"]
        for dir in dirs:
            try:
                os.makedirs(dir, exist_ok=True)
                self.print_status("DIR", f"Created: {dir}/", "SUCCESS")
            except:
                self.print_status("DIR", f"Exists: {dir}/", "INFO")

    def main(self):
        try:
            self.print_banner()
            
            # Run system checks
            if not self.check_python():
                return False
                
            self.check_platform()
            
            # Check file structure
            if not self.check_file_structure():
                self.print_status("INSTALL", "File structure check failed", "WARNING")
                # Continue anyway since tool might still work
                
            self.upgrade_pip()
            
            if not self.install_requirements():
                return False
                
            if not self.verify_installation():
                return False
                
            self.create_dirs()
            
            duration = datetime.now() - self.start_time
            print(f"\n{Fore.GREEN}✅ Installation completed in {duration.total_seconds():.1f}s")
            print(f"\n{Fore.YELLOW}🚀 Usage:")
            print(f"{Fore.WHITE}  python numintense_pro.py +919876543210")
            print(f"{Fore.WHITE}  python numintense_pro.py +919876543210 --full")
            print(f"{Fore.WHITE}  python numintense_pro.py admin@example.com --email")
            print(f"{Fore.WHITE}  python numintense_pro.py example.com --domain")
            
            print(f"\n{Fore.CYAN}💡 Quick Test:")
            print(f"{Fore.WHITE}  python numintense_pro.py +919876543210 --quiet")
            
            return True
            
        except KeyboardInterrupt:
            self.print_status("INSTALL", "Interrupted by user", "WARNING")
            return False
        except Exception as e:
            self.print_status("INSTALL", f"Error: {e}", "ERROR")
            return False

if __name__ == "__main__":
    installer = NumIntenseInstaller()
    success = installer.main()
    
    if not success:
        print(f"\n{Fore.RED}💡 Troubleshooting:")
        print(f"{Fore.YELLOW}1. Check internet connection")
        print(f"{Fore.YELLOW}2. Try: pip install --upgrade pip")
        print(f"{Fore.YELLOW}3. Run as admin/sudo if needed")
        print(f"{Fore.YELLOW}4. Check if requirements.txt exists")
        sys.exit(1)