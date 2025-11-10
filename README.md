```markdown
# 🔍 NumIntense - Advanced OSINT & Phone Intelligence Tool

**NumIntense** is a powerful open-source Python CLI tool for **OSINT (Open Source Intelligence)** and **phone number intelligence**.  
It helps ethical hackers, cybersecurity researchers, and digital investigators extract detailed information.

## ⚡ Features

- 🌍 **Phone Number Intelligence** - Country, carrier, timezone, validation
- 🔎 **Social Media OSINT** - Facebook, Telegram, Truecaller links
- 🛡️ **Spam Detection** - Multiple spam database checks
- 📧 **Email Forensics** - Breach checking and analysis
- 🌐 **Domain Intelligence** - WHOIS lookup and domain info
- 🎯 **Cross-Platform** - Works on Termux, Kali Linux, Windows, macOS

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/numintense.git
cd numintense

# Run installer
python install.py

# Basic usage
python numintense.py +919876543210

# Full OSINT scan
python numintense.py +919876543210 --full

# Email check
python numintense.py admin@company.com --email

# Domain check  
python numintense.py example.com --domain
```

📋 Usage Examples

```bash
# Basic phone intelligence
python numintense.py +919876543210

# Comprehensive investigation
python numintense.py +919876543210 --full

# Email breach check
python numintense.py target@email.com --email

# Domain information
python numintense.py target.com --domain

# Quiet mode (no banner)
python numintense.py +919876543210 --quiet
```

🛠️ Requirements

· Python 3.6+
· pip package manager
· Internet connection

📦 Dependencies

· phonenumbers - Phone number parsing
· requests - HTTP requests
· colorama - Terminal colors
· whois - Domain lookup

🐧 Platform Support

· ✅ Termux (Android)
· ✅ Kali Linux
· ✅ Ubuntu/Debian
· ✅ Windows 10/11
· ✅ macOS

⚖️ Legal Disclaimer

This tool is for authorized security research only. Users must comply with all applicable laws and regulations. Respect privacy and obtain proper authorization before use.

🐛 Reporting Issues

Found a bug? Please create an issue on GitHub with:

· Error message
· Python version
· Operating system
· Steps to reproduce

🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

📄 License

MIT License - see LICENSE file for details.

---

NumIntense - Empowering open-source OSINT for everyone 🔍

```

**6. LICENSE FILE:**
**Filename:** `LICENSE`
```python
MIT License

Copyright (c) 2024 GulsHan Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
