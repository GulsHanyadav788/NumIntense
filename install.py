#!/usr/bin/env python3

import sys
import subprocess
import os
from colorama import Fore, Style, init

init(autoreset=True)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print(Fore.RED + "[!] Python 3.6 or higher is required")
        sys.exit(1)
    print(Fore.GREEN + f"[✓] Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(Fore.RED + f"[!] {requirements_file} not found")
        sys.exit(1)
    
    print(Fore.CYAN + "[📦] Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print(Fore.GREEN + "[✓] All dependencies installed successfully")
        
    except subprocess.CalledProcessError:
        print(Fore.RED + "[!] Failed to install dependencies")
        sys.exit(1)

def verify_installation():
    """Verify that all packages are installed correctly"""
    packages = ["phonenumbers", "requests", "colorama", "whois"]
    missing = []
    
    for package in packages:
        try:
            __import__(package)
            print(Fore.GREEN + f"[✓] {package} installed")
        except ImportError:
            missing.append(package)
            print(Fore.RED + f"[!] {package} missing")
    
    if missing:
        print(Fore.RED + f"[!] Missing packages: {', '.join(missing)}")
        return False
    
    print(Fore.GREEN + "[✓] All packages verified successfully")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["modules", "apis"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(Fore.GREEN + f"[✓] Created directory: {directory}/")
        else:
            print(Fore.YELLOW + f"[!] Directory already exists: {directory}/")

def main():
    print(Fore.CYAN + "🔧 NumIntense Pro - Installation Script")
    print(Fore.CYAN + "=" * 50)
    
    check_python_version()
    create_directories()
    install_requirements()
    
    if verify_installation():
        print(Fore.GREEN + "\n🎉 Installation completed successfully!")
        print(Fore.YELLOW + "\nUsage examples:")
        print(Fore.WHITE + "  python main.py +919876543210")
        print(Fore.WHITE + "  python main.py target@example.com --email")
        print(Fore.WHITE + "  python main.py example.com --domain")
        print(Fore.WHITE + "  python main.py +919876543210 --all --save")
    else:
        print(Fore.RED + "\n❌ Installation failed!")

if __name__ == "__main__":
    main()