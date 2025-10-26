NumIntense Pro 🔍

Advanced Phone Number & Digital Footprint OSINT Intelligence Tool

https://img.shields.io/badge/Python-3.6%2B-blue
https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Termux%20%7C%20Windows%20%7C%20macOS-green
https://img.shields.io/badge/License-MIT-yellow

🌟 Overview

NumIntense Pro is a comprehensive OSINT (Open Source Intelligence) framework designed for advanced phone number investigation and digital footprint analysis. It combines multiple intelligence sources into a single, powerful tool for security researchers, penetration testers, and digital investigators.

🚀 Features

📞 Phone Number Intelligence

· Basic Information: Carrier, location, timezone, number type
· International Format Support: Automatic country code detection
· Validation & Parsing: Advanced phone number validation using Google's libphonenumber
· Multi-format Output: E164, International, and National formats

🔍 OSINT Integration

· Facebook Investigation: Profile search, group discovery, and advanced dorks
· Telegram Lookup: Username generation and direct profile links
· Truecaller Integration: Multi-source reverse phone lookup
· Spam Detection: Comprehensive spam database checks
· Search Automation: Advanced Google dork generation

📧 Digital Footprint Analysis

· Email Breach Checking: Have I Been Pwned integration
· Domain Intelligence: WHOIS lookups and registration details
· Social Media Presence: Multi-platform account discovery

💾 Advanced Capabilities

· Batch Processing: Multiple targets in single operation
· Report Generation: Professional text reports
· API Integration: Extensible plugin system
· Rate Limiting: Responsible API usage
· Cross-Platform: Works on Kali Linux, Termux, Windows, and macOS

🛠 Installation

Quick Install (Recommended)

```bash
# Download all project files to a directory, then run:
python install.py
```

Manual Installation

```bash
# Install dependencies
pip install phonenumbers requests colorama whois python-whois beautifulsoup4 lxml urllib3

# Or using requirements file
pip install -r requirements.txt

# Verify installation
python main.py --help
```

Platform-Specific Instructions

Kali Linux

```bash
sudo apt update
sudo apt install python3 python3-pip -y
python3 install.py
```

Termux (Android)

```bash
pkg update && pkg install python -y
python install.py
```

Windows

```bash
# Ensure Python 3.6+ is installed from python.org
python install.py
```

macOS

```bash
# Ensure Python 3.6+ is installed
python3 install.py
```

📖 Usage Examples

Basic Phone Number Investigation

```bash
python main.py +919876543210
```

Comprehensive OSINT Analysis

```bash
python main.py +919876543210 --all --save --verbose
```

Email Security Check

```bash
python main.py target@example.com --email
```

Domain Intelligence

```bash
python main.py example.com --domain
```

Quick Scan (Quiet Mode)

```bash
python main.py +919876543210 --quiet
```

⚙️ Configuration

API Keys Setup (Optional)

Edit config.json to enhance functionality:

```json
{
    "apis": {
        "numverify": "YOUR_NUMVERIFY_API_KEY",
        "abstractapi": "YOUR_ABSTRACTAPI_KEY", 
        "hibp": "YOUR_HIBP_API_KEY"
    },
    "settings": {
        "rate_limit_delay": 1,
        "timeout": 10,
        "save_reports": false
    }
}
```

Getting API Keys (Optional)

1. NumVerify: https://numverify.com (Free tier available)
2. AbstractAPI: https://abstractapi.com (Free tier available)
3. Have I Been Pwned: https://haveibeenpwned.com/API/Key

🎯 Command Line Options

Option Description Example
target Phone number, email, or domain +919876543210
--all Run all available checks --all
--save Save results to files --save
--verbose Enable detailed output --verbose
--quiet Minimal output --quiet
--email Target is email address --email
--domain Target is domain --domain
--config Custom config file --config myconfig.json

📊 Sample Output

Phone Number Analysis

```
📞 BASIC INFORMATION:
  ✅ Number: +91 98765 43210 (India)
  ✅ Carrier: Airtel
  ✅ Timezone: Asia/Kolkata
  ✅ Type: Mobile
  ✅ Valid: Yes

🔍 OSINT RESULTS:
  ✅ Facebook: 5 search variations generated
  ✅ Telegram: 12 username variations checked
  ✅ Spam: 15 databases queried
  ✅ Truecaller: 8 lookup sources scanned
```

Email Security Report

```
📧 EMAIL BREACH REPORT: user@example.com
  ✅ HIBP: No breaches found
  ⚠️ Recommendations: Enable 2FA, use password manager
```

Domain Intelligence

```
🌐 WHOIS REPORT: example.com
  ✅ Registrar: GoDaddy
  ✅ Created: 2020-01-01
  ✅ Expires: 2024-01-01
  ✅ Status: Active
```

🏗 Project Structure

```
numintense_pro/
├── main.py                 # Main application
├── install.py             # Installation script
├── requirements.txt       # Dependencies
├── config.json           # Configuration
├── modules/              # Core modules
│   ├── email_breach_check.py
│   ├── facebook_check.py
│   ├── generate_dorks.py
│   ├── spam_check.py
│   ├── telegram_lookup.py
│   ├── truecaller_lookup.py
│   └── whois_lookup.py
└── apis/                 # API integrations
    ├── numverify.py
    └── abstractapi.py
```

🔧 Modules Overview

Core Intelligence Modules

· Phone Intelligence: Basic number analysis and validation
· Facebook OSINT: Social media investigation with advanced dorks
· Telegram Lookup: Smart username generation and profile discovery
· Truecaller Integration: Multi-source reverse phone lookup
· Spam Detection: 15+ spam database checks
· Email Security: HIBP breach checking
· Domain Intelligence: WHOIS registration data
· Dork Generation: Automated search query creation

API Integrations

· NumVerify: Phone number validation API
· AbstractAPI: Additional phone intelligence services
· Have I Been Pwned: Email breach database

🛡 Legal & Ethical Usage

✅ Permitted Uses

· Security research and penetration testing
· Digital forensics and investigations
· Personal security awareness
· Educational purposes
· Authorized red team operations
· Bug bounty hunting

❌ Prohibited Uses

· Harassment or stalking
· Unauthorized surveillance
· Commercial spam operations
· Illegal activities
· Violating terms of service
· Impersonation or fraud

⚠️ Important Disclaimer

This tool is designed for authorized security testing and educational purposes only. Users are solely responsible for complying with applicable laws and regulations. Always obtain proper authorization before conducting any investigations. The developers are not responsible for any misuse of this tool.

🐛 Troubleshooting

Common Issues & Solutions

1. Module Import Errors
   ```bash
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt
   ```
2. Python Version Issues
   ```bash
   # Check Python version
   python --version
   # Requires Python 3.6 or higher
   ```
3. Network Connectivity
   ```bash
   # Test basic connectivity
   python -c "import requests; print(requests.get('https://google.com').status_code)"
   ```
4. Permission Issues (Linux/macOS)
   ```bash
   # Use virtual environment
   python -m venv numintense_env
   source numintense_env/bin/activate
   pip install -r requirements.txt
   ```

Debug Mode

```bash
python main.py +1234567890 --verbose
```

🔄 Updates & Maintenance

Checking for Updates

```bash
# If using git
git pull origin main
python install.py

# Otherwise, re-download latest files and run:
python install.py
```

Adding Custom Modules

1. Create new module in modules/ directory
2. Follow existing module structure
3. Import in main.py
4. Add to appropriate function calls

🤝 Contributing

We welcome contributions from the security community! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow the existing code style
5. Include updated documentation
6. Test your changes thoroughly

Development Setup

```bash
git clone <repository-url>
cd numintense_pro
python install.py
python main.py --help
```

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

· Google for libphonenumber library
· Have I Been Pwned for breach data services
· NumVerify for phone validation API
· AbstractAPI for additional intelligence services
· Open Source Community for continuous improvements and feedback

📞 Support & Resources

Documentation

· In-line code documentation and comments
· Example configurations in config.json
· Comprehensive help via --help flag

Issue Reporting

When reporting issues, please include:

1. Your operating system and Python version
2. Exact command used
3. Full error message/output
4. Steps to reproduce the issue

Community Guidelines

· Be respectful and professional
· Share knowledge and techniques
· Report vulnerabilities responsibly
· Help improve tool detection and prevention

---

🎯 Quick Start Cheat Sheet

```bash
# Installation
python install.py

# Basic usage
python main.py +1234567890

# Full investigation
python main.py +1234567890 --all --save

# Email check
python main.py admin@company.com --email

# Domain check  
python main.py target.com --domain

# Quiet mode for quick scans
python main.py +1234567890 --quiet
```

---

NumIntense Pro - Your comprehensive digital investigation companion.

Remember: With great power comes great responsibility. Always respect privacy, follow laws, and use this tool ethically. 🔍

Stay curious, stay ethical, stay secure.