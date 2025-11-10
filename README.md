# 🔍 NumIntense - Advanced OSINT & Phone Intelligence Tool

**NumIntense** is a powerful open-source Python CLI tool for **OSINT (Open Source Intelligence)** and **phone number intelligence**.  
Developed by **GulsHan Yadav**, it helps ethical hackers, cybersecurity researchers, and digital investigators extract detailed information about phone numbers, emails, and domains.

## ⚡ Features

- 🌍 **Phone Number Intelligence** - Country, carrier, timezone, validation
- 🔎 **Social Media OSINT** - Facebook, Telegram, Instagram, LinkedIn lookup
- 🛡️ **Spam Detection** - Multiple spam database checks
- 📧 **Email Forensics** - Breach checking and analysis
- 🌐 **Domain Intelligence** - WHOIS lookup and domain information
- 🎯 **Advanced Dorking** - Google dork generation for deep research
- 📊 **Comprehensive Reports** - Professional investigation summaries
- 🖥️ **Cross-Platform** - Works on Termux, Kali Linux, Windows, macOS

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- pip package manager
- Internet connection

### Installation

**Option 1: Automated Installation (Recommended)**
```bash
# Linux/Mac/Termux
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

Option 2: Manual Installation

```bash
# Clone or download the tool
git clone https://github.com/GulsHanyadav788/numintense.git
cd numintense

# Run installer
python install.py

# Verify installation
python numintense_pro.py --help
```

📋 Usage Examples

Basic Phone Intelligence

```bash
python numintense_pro.py +919876543210
```

Output: Basic carrier, country, timezone, and validation information

Full OSINT Scan

```bash
python numintense_pro.py +919876543210 --full
```

Output: Comprehensive intelligence including social media, spam databases, and advanced lookup

Email Investigation

```bash
python numintense_pro.py target@email.com --email
```

Output: Breach checks, social media presence, and domain analysis

Domain Intelligence

```bash
python numintense_pro.py example.com --domain
```

Output: WHOIS information, registration details, and domain metadata

Quiet Mode (No Banner)

```bash
python numintense_pro.py +919876543210 --quiet
```

Output: Minimal output without banner for automated operations

🛠️ Advanced Features

Module System

NumIntense includes specialized modules for different intelligence tasks:

· Email Intelligence (modules/email_check.py)
· Social Media OSINT (modules/social_osint.py)
· Advanced Dorking (modules/advanced_dorks.py)
· Secure API Integration (apis/secure_api.py)

Configuration

Edit config.json to customize:

· API keys for enhanced services
· Rate limiting settings
· Output preferences
· Stealth mode options

```json
{
    "api_configuration": {
        "numverify": "YOUR_API_KEY_HERE",
        "abstractapi": "YOUR_API_KEY_HERE"
    },
    "operation_settings": {
        "rate_limit_delay": 1,
        "save_reports": false
    }
}
```

🎯 Output Example

```
📊 BASIC INFORMATION
────────────────────────
📱 Number: +91 98765 43210
🔢 E164: +919876543210
🌍 Country: India (IN)
🏢 Carrier: Airtel
🕐 Timezone: Asia/Kolkata
✅ Validation: ✅ Valid
🔧 Type: 📱 Mobile

🔍 SOCIAL MEDIA OSINT
────────────────────────
📱 Facebook: https://www.facebook.com/search/top/?q=919876543210
📱 Telegram: https://t.me/919876543210
📱 Truecaller: https://www.truecaller.com/search/919876543210

🎉 INVESTIGATION COMPLETE!
────────────────────────
📋 Case ID: NI-20241201-143052-ABC123
⏱️ Completed: 14:30:55
📊 Modules: Basic + OSINT
```

🐧 Platform Support

Platform Status Notes
✅ Termux (Android) Fully Supported Optimal for mobile investigations
✅ Kali Linux Fully Supported Perfect for penetration testing
✅ Ubuntu/Debian Fully Supported Standard Linux distributions
✅ Windows 10/11 Fully Supported Native CMD/PowerShell support
✅ macOS Fully Supported Terminal and iTerm support
✅ Parrot OS Fully Supported Security-focused distribution

📦 Dependencies

NumIntense requires these Python packages:

· phonenumbers - Advanced phone number parsing
· requests - HTTP requests and API calls
· colorama - Cross-platform colored terminal output
· whois - Domain information lookup

All dependencies are automatically installed via requirements.txt.

🔧 Troubleshooting

Common Issues

1. Python Not Found

```bash
# Check Python installation
python --version
python3 --version

# Install Python if missing (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip
```

2. Permission Denied

```bash
# Make scripts executable
chmod +x setup.sh
chmod +x numintense_pro.py
```

3. Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

4. Termux Issues

```bash
# Update Termux packages
pkg update && pkg upgrade

# Install Python in Termux
pkg install python
```

Getting Help

1. Check the #troubleshooting section in this README
2. Review the installation logs in logs/ directory
3. Ensure all dependencies are properly installed
4. Verify internet connectivity for API calls

🤝 Contributing

We welcome contributions! Here's how you can help:

Reporting Bugs

1. Check existing issues on GitHub
2. Create a new issue with:
   · Error message and stack trace
   · Python version (python --version)
   · Operating system
   · Steps to reproduce

Feature Requests

1. Open an issue with "[FEATURE]" prefix
2. Describe the use case and expected behavior
3. Provide examples if possible

Code Contributions

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

📁 Project Structure

```
numintense/
├── numintense_pro.py      # 🎯 MAIN EXECUTABLE
├── install.py            # 🔧 INSTALLATION
├── requirements.txt      # 📦 DEPENDENCIES
├── config.json          # ⚙️ CONFIGURATION
├── README.md           # 📚 DOCUMENTATION
├── LICENSE             # 📄 LICENSE
├── setup.sh           # 🐧 LINUX/MAC SETUP
├── setup.bat          # 🪟 WINDOWS SETUP
├── modules/           # 🛠️ INTELLIGENCE MODULES
│   ├── email_check.py
│   ├── social_osint.py
│   └── advanced_dorks.py
├── apis/              # 🔌 API INTEGRATIONS
│   └── secure_api.py
└── utils/             # 🧰 UTILITIES
    └── helpers.py
```

⚖️ Legal Disclaimer

⚠️ IMPORTANT: LEGAL COMPLIANCE

This tool is designed for:

· ✅ Authorized Security Research
· ✅ Ethical Hacking with Permission
· ✅ Digital Forensics Investigations
· ✅ Cybersecurity Education
· ✅ Personal Security Awareness

PROHIBITED USES:

· ❌ Unauthorized access to systems
· ❌ Harassment or stalking
· ❌ Illegal surveillance
· ❌ Commercial exploitation without permission
· ❌ Any activity violating local laws

Users are solely responsible for:

· Ensuring proper authorization before use
· Compliance with all applicable laws
· Respecting privacy and data protection regulations
· Ethical use of gathered information

By using this tool, you agree to use it only for legitimate, authorized purposes.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🏆 Credits

Developer: GulsHan Yadav
Security Research: NumIntense Team
Special Thanks: Open-source community contributors

🌟 Support the Project

If you find NumIntense useful, please consider:

1. ⭐ Starring the repository on GitHub
2. 🐛 Reporting issues and bugs
3. 💡 Suggesting new features
4. 🔄 Sharing with colleagues
5. 🏗️ Contributing code improvements

🔗 Links

· GitHub Repository: https://github.com/GulsHanyadav788/numintense
· Issue Tracker: https://github.com/GulsHanyadav788/numintense/issues
· Releases: https://github.com/GulsHanyadav788/numintense/releases

---

NumIntense - Empowering open-source OSINT for everyone 🔍

"Knowledge is power, but ethics give it purpose." - GulsHan Yadav

```
