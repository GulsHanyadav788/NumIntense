#!/bin/bash
echo "🔍 NumIntense - Installation Script"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.6+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python $python_version detected"

# Run installer
echo "🚀 Starting installation..."
python3 install.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "Quick start:"
    echo "  python3 numintense.py +919876543210"
    echo "  python3 numintense.py +919876543210 --full"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check the errors above."
    exit 1
fi