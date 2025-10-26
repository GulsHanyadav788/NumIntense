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
· Report Generation: Professional PDF and text reports
· API Integration: Extensible plugin system
· Rate Limiting: Responsible API usage
· Cross-Platform: Works on Kali Linux, Termux, Windows, and macOS

🛠 Installation

Quick Install (Recommended)

```bash
# Clone or download the project files
# Run the automated installer
python install.py
```

Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python main.py --help
```

Platform-Specific Instructions

Kali Linux

```bash
sudo apt update
python install.py
```

Termux (Android)

```bash
pkg update && pkg install python
python install.py
```

Windows

```bash
# Ensure Python 3.6+ is installed
python install.py
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

Batch Processing

```bash
# Create a targets file
echo "+919876543210" > targets.txt
echo "+11234567890" >> targets.txt
echo "admin@company.com" >> targets.txt

# Process all targets
python main.py --batch targets.txt
```

⚙️ Configuration

API Keys Setup

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
        "save_reports": true
    }
}
```

Getting API Keys

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
--batch Process multiple targets --batch targets.txt

📊 Output Examples

Phone Number Analysis

```
📞 BASIC INFORMATION:
  ✅ Number: +91 98765 43210 (India)
  ✅ Carrier: Airtel
  ✅ Timezone: Asia/Kolkata
  ✅ Type: Mobile
  ✅ Valid: Yes

🔍 OSINT RESULTS:
  ✅ Facebook: 3 potential profiles
  ✅ Telegram: 2 username variations
  ✅ Spam: No reports found
  ✅ Breaches: Clean record
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
  ✅ Created: 2020-01-01 (3 years old)
  ✅ Expires: 2024-01-01 (180 days)
  ✅ Name Servers: ns1.example.com, ns2.example.com
```

🏗 Architecture

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

Core Modules

· Phone Intelligence: Basic number analysis and validation
· Facebook OSINT: Social media investigation
· Telegram Lookup: Messenger profile discovery
· Truecaller Integration: Reverse phone lookup
· Spam Detection: Multi-source spam databases
· Email Security: Breach monitoring
· Domain Intelligence: WHOIS and registration data
· Dork Generation: Advanced search automation

API Integrations

· NumVerify: Phone number validation
· AbstractAPI: Additional phone intelligence
· Have I Been Pwned: Email breach checking

🛡 Legal & Ethical Usage

✅ Permitted Uses

· Security research and penetration testing
· Digital forensics and investigations
· Personal security awareness
· Educational purposes
· Authorized red team operations

❌ Prohibited Uses

· Harassment or stalking
· Unauthorized surveillance
· Commercial spam operations
· Illegal activities
· Violating terms of service

Disclaimer

This tool is designed for authorized security testing and educational purposes only. Users are responsible for complying with applicable laws and regulations. Always obtain proper authorization before conducting any investigations.

🐛 Troubleshooting

Common Issues

1. Module Import Errors
   ```bash
   pip install --upgrade -r requirements.txt
   ```
2. API Rate Limiting
   · Increase rate_limit_delay in config
   · Use API keys for higher limits
3. Network Connectivity
   ```bash
   # Test API connectivity
   python -c "import requests; print(requests.get('https://api.numverify.com').status_code)"
   ```

Debug Mode

```bash
python main.py +1234567890 --verbose
```

🔄 Updates & Maintenance

Checking for Updates

```bash
git pull origin main
python install.py
```

Adding New Modules

1. Create module in modules/ directory
2. Import in main.py
3. Add to appropriate function calls

🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow the code style guide
5. Include documentation updates

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
· Have I Been Pwned for breach data
· NumVerify for phone validation API
· AbstractAPI for additional services
· Open Source Community for continuous improvements

📞 Support

Documentation

· Full documentation available in code comments
· Example usage in EXAMPLES.md
· Configuration guide in CONFIG.md

Issues

Report bugs and feature requests:

1. Check existing issues
2. Create detailed bug report
3. Include system information
4. Provide error logs

Community

· GitHub Discussions for questions
· Wiki for tutorials and guides
· Issue tracker for bugs

---

NumIntense Pro - Your comprehensive digital investigation companion. Use responsibly. 🔍

Remember: With great power comes great responsibility. Always respect privacy and legal boundaries.