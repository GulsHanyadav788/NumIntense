#!/usr/bin/env python3

"""
🔥 NumIntense Pro - Enterprise Installation System
Description: Automated deployment for Ultimate OSINT Intelligence Suite
Version: 3.0.0 | Deployment Engine
Author: GulsHan Kumar & Security Research Team
"""

import sys
import subprocess
import os
import platform
import time
from datetime import datetime
from colorama import init, Fore, Style, Back

# Initialize colorama
init(autoreset=True)

class NumIntenseInstaller:
    def __init__(self):
        self.start_time = datetime.now()
        self.platform = platform.system().lower()
        self.architecture = platform.architecture()[0]
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
    def print_banner(self):
        """Display professional installation banner"""
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
    ║                    🔥 ENTERPRISE DEPLOYMENT SYSTEM                          ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
        """)
        
        print(Fore.CYAN + Style.BRIGHT + "    " + "═" * 70)
        print(Fore.YELLOW + f"    🚀 Version 3.0.0 | Deployment Engine | {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(Fore.GREEN + f"    🖥️  Platform: {self.platform.title()} {self.architecture} | Python: {self.python_version}")
        print(Fore.CYAN + "    " + "═" * 70)
        print()

    def print_status(self, step, message, status="INFO"):
        """Print formatted status messages"""
        status_config = {
            "SUCCESS": {"color": Fore.GREEN, "icon": "✅", "label": "SUCCESS"},
            "ERROR": {"color": Fore.RED, "icon": "❌", "label": "ERROR"},
            "WARNING": {"color": Fore.YELLOW, "icon": "⚠️", "label": "WARNING"},
            "INFO": {"color": Fore.CYAN, "icon": "🔹", "label": "INFO"},
            "PROCESSING": {"color": Fore.BLUE, "icon": "🔄", "label": "PROCESSING"},
            "DOWNLOAD": {"color": Fore.MAGENTA, "icon": "📦", "label": "DOWNLOAD"}
        }
        
        config = status_config.get(status, status_config["INFO"])
        print(f"{config['color']}{config['icon']} [{step}] {message}")

    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_status("SYSTEM", "Checking Python environment...", "PROCESSING")
        
        if sys.version_info < (3, 6):
            self.print_status("PYTHON", "Python 3.6 or higher is required", "ERROR")
            self.print_status("PYTHON", f"Current version: {self.python_version}", "ERROR")
            return False
        
        self.print_status("PYTHON", f"Version {self.python_version} verified", "SUCCESS")
        return True

    def check_platform_compatibility(self):
        """Check platform compatibility"""
        self.print_status("SYSTEM", "Checking platform compatibility...", "PROCESSING")
        
        supported_platforms = ['linux', 'darwin', 'windows']
        if self.platform not in supported_platforms:
            self.print_status("PLATFORM", f"Unsupported platform: {self.platform}", "WARNING")
            self.print_status("PLATFORM", "Supported platforms: Linux, macOS, Windows", "INFO")
        else:
            self.print_status("PLATFORM", f"{self.platform.title()} detected", "SUCCESS")
        
        return True

    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        self.print_status("SETUP", "Upgrading package manager...", "PROCESSING")
        
        try:
            # Run pip upgrade silently
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.print_status("PIP", "Package manager upgraded successfully", "SUCCESS")
            else:
                self.print_status("PIP", "Pip upgrade completed with warnings", "WARNING")
                
        except subprocess.TimeoutExpired:
            self.print_status("PIP", "Pip upgrade timeout - continuing anyway", "WARNING")
        except Exception as e:
            self.print_status("PIP", f"Pip upgrade failed: {e}", "WARNING")

    def install_requirements(self):
        """Install required packages with enhanced error handling"""
        requirements_file = "requirements.txt"
        
        if not os.path.exists(requirements_file):
            self.print_status("DEPENDENCIES", f"Requirements file not found: {requirements_file}", "ERROR")
            return False
        
        self.print_status("DEPENDENCIES", "Installing core dependencies...", "DOWNLOAD")
        
        try:
            # Show progress for installation
            process = subprocess.Popen([
                sys.executable, "-m", "pip", "install", "-r", requirements_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Real-time output handling
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # Filter and show meaningful output
                    if "Successfully installed" in output or "Requirement already satisfied" in output:
                        print(f"    {Fore.GREEN}📦 {output.strip()}")
            
            return_code = process.poll()
            
            if return_code == 0:
                self.print_status("DEPENDENCIES", "All dependencies installed successfully", "SUCCESS")
                return True
            else:
                self.print_status("DEPENDENCIES", "Dependency installation completed with errors", "ERROR")
                return False
                
        except subprocess.CalledProcessError as e:
            self.print_status("DEPENDENCIES", f"Installation failed: {e}", "ERROR")
            return False
        except Exception as e:
            self.print_status("DEPENDENCIES", f"Unexpected error: {e}", "ERROR")
            return False

    def verify_installation(self):
        """Verify that all packages are installed correctly"""
        self.print_status("VERIFICATION", "Verifying installation...", "PROCESSING")
        
        # Core dependencies
        core_packages = {
            "phonenumbers": "Phone number intelligence",
            "requests": "HTTP operations",
            "colorama": "Terminal styling",
            "whois": "Domain intelligence"
        }
        
        # Optional dependencies
        optional_packages = {
            "beautifulsoup4": "Web scraping (Optional)",
            "lxml": "XML processing (Optional)",
            "cryptography": "Security features (Optional)"
        }
        
        all_success = True
        missing_core = []
        
        # Check core packages
        for package, description in core_packages.items():
            try:
                __import__(package)
                self.print_status("VERIFY", f"{package}: {description}", "SUCCESS")
            except ImportError:
                missing_core.append(package)
                self.print_status("VERIFY", f"{package}: {description}", "ERROR")
                all_success = False
        
        # Check optional packages
        for package, description in optional_packages.items():
            try:
                __import__(package)
                self.print_status("VERIFY", f"{package}: {description}", "SUCCESS")
            except ImportError:
                self.print_status("VERIFY", f"{package}: {description}", "WARNING")
        
        if missing_core:
            self.print_status("VERIFICATION", f"Missing core packages: {', '.join(missing_core)}", "ERROR")
            return False
        
        self.print_status("VERIFICATION", "All core dependencies verified", "SUCCESS")
        return all_success

    def create_directories(self):
        """Create necessary directory structure"""
        self.print_status("SETUP", "Creating project structure...", "PROCESSING")
        
        directories = [
            "modules",      # Core intelligence modules
            "apis",         # API integrations
            "reports",      # Investigation reports
            "data",         # Cache and temporary data
            "logs"          # Operation logs
        ]
        
        for directory in directories:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    self.print_status("DIRECTORY", f"Created: {directory}/", "SUCCESS")
                else:
                    self.print_status("DIRECTORY", f"Exists: {directory}/", "INFO")
            except Exception as e:
                self.print_status("DIRECTORY", f"Failed to create {directory}: {e}", "ERROR")

    def check_file_structure(self):
        """Verify essential files exist"""
        self.print_status("SETUP", "Verifying file structure...", "PROCESSING")
        
        essential_files = [
            "main.py",
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

    def run_system_checks(self):
        """Run comprehensive system checks"""
        self.print_status("SYSTEM", "Running comprehensive system diagnostics...", "PROCESSING")
        
        checks = [
            ("Python Version", self.check_python_version),
            ("Platform Compatibility", self.check_platform_compatibility),
            ("File Structure", self.check_file_structure),
            ("Directory Structure", self.create_directories)
        ]
        
        for check_name, check_function in checks:
            if not check_function():
                self.print_status("SYSTEM", f"Check failed: {check_name}", "ERROR")
                return False
            time.sleep(0.5)  # Visual delay
        
        return True

    def print_installation_summary(self, success):
        """Print installation summary"""
        duration = datetime.now() - self.start_time
        print(f"\n{Fore.CYAN}{Style.BRIGHT}    📊 INSTALLATION SUMMARY")
        print(Fore.CYAN + "    " + "─" * 50)
        
        if success:
            print(f"    {Fore.GREEN}✅ Installation Status: {Fore.WHITE}COMPLETED SUCCESSFULLY")
            print(f"    {Fore.GREEN}⏱️  Duration: {Fore.WHITE}{duration.total_seconds():.1f} seconds")
            print(f"    {Fore.GREEN}🐍 Python Version: {Fore.WHITE}{self.python_version}")
            print(f"    {Fore.GREEN}🖥️  Platform: {Fore.WHITE}{self.platform.title()} {self.architecture}")
            print(f"    {Fore.GREEN}📁 Project Structure: {Fore.WHITE}Ready")
            print(f"    {Fore.GREEN}📦 Dependencies: {Fore.WHITE}Installed and Verified")
            
            print(f"\n{Fore.YELLOW}    🚀 READY TO DEPLOY:")
            print(f"    {Fore.WHITE}    python main.py +1234567890")
            print(f"    {Fore.WHITE}    python main.py +1234567890 --full-scan --save")
            print(f"    {Fore.WHITE}    python main.py admin@company.com --email")
            print(f"    {Fore.WHITE}    python main.py target.com --domain")
            
        else:
            print(f"    {Fore.RED}❌ Installation Status: {Fore.WHITE}FAILED")
            print(f"    {Fore.RED}⏱️  Duration: {Fore.WHITE}{duration.total_seconds():.1f} seconds")
            print(f"    {Fore.RED}💡 Check the errors above and try again")
        
        print(Fore.CYAN + "    " + "─" * 50)

    def main(self):
        """Main installation routine"""
        try:
            # Display banner
            self.print_banner()
            
            # Run system checks
            if not self.run_system_checks():
                self.print_status("INSTALLATION", "System checks failed", "ERROR")
                self.print_installation_summary(False)
                return False
            
            # Upgrade pip
            self.upgrade_pip()
            
            # Install requirements
            if not self.install_requirements():
                self.print_status("INSTALLATION", "Dependency installation failed", "ERROR")
                self.print_installation_summary(False)
                return False
            
            # Verify installation
            if not self.verify_installation():
                self.print_status("INSTALLATION", "Installation verification failed", "ERROR")
                self.print_installation_summary(False)
                return False
            
            # Final success
            self.print_installation_summary(True)
            return True
            
        except KeyboardInterrupt:
            self.print_status("INSTALLATION", "Installation interrupted by user", "WARNING")
            self.print_installation_summary(False)
            return False
        except Exception as e:
            self.print_status("INSTALLATION", f"Unexpected error: {e}", "ERROR")
            self.print_installation_summary(False)
            return False

if __name__ == "__main__":
    installer = NumIntenseInstaller()
    success = installer.main()
    
    if not success:
        print(f"\n{Fore.RED}💡 Troubleshooting Tips:")
        print(f"{Fore.YELLOW}1. Ensure you have internet connectivity")
        print(f"{Fore.YELLOW}2. Try: pip install --upgrade pip")
        print(f"{Fore.YELLOW}3. Check Python version: python --version")
        print(f"{Fore.YELLOW}4. Run with admin/sudo privileges if needed")
        print(f"{Fore.YELLOW}5. Check the requirements.txt file exists")
        
        sys.exit(1)