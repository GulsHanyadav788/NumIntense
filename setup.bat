@echo off
chcp 65001 >nul
echo 🔍 NumIntense - Installation Script
echo ======================================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.6+ first.
    pause
    exit /b 1
)

echo ✅ Python detected
echo 🚀 Starting installation...
python install.py

if errorlevel 1 (
    echo.
    echo ❌ Installation failed. Please check the errors above.
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 Installation completed successfully!
    echo.
    echo Quick start:
    echo   python numintense_pro.py +919876543210        :: ✅ CHANGED
    echo   python numintense_pro.py +919876543210 --full :: ✅ CHANGED
    echo.
)
pause