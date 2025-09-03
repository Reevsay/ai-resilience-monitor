@echo off
echo 🔧 API Key Setup Helper
echo =====================
echo.

echo 📝 You need to get valid API keys. Here's how:
echo.

echo 🤗 HUGGING FACE (Free):
echo 1. Go to: https://huggingface.co/settings/tokens
echo 2. Click "New token"
echo 3. Name: "AI-Resilience-Project"
echo 4. Role: "Read"
echo 5. Copy the token (starts with "hf_")
echo.

echo 🧠 GOOGLE GEMINI (Free):
echo 1. Go to: https://makersuite.google.com/app/apikey
echo 2. Click "Create API key"
echo 3. Copy the key (starts with "AIzaSy" and is about 39 characters)
echo 4. Make sure you DON'T copy the website URL part!
echo.

echo 📋 CURRENT STATUS:
echo Your Hugging Face key: your_key_here (possibly expired/rate limited)
echo Your Gemini key: INVALID (contains URL fragment)
echo.

echo 🚀 ALTERNATIVE: Let's add Ollama (Local AI) first!
echo This runs completely on your machine - no API keys needed!
echo.

set /p choice="Would you like to (1) Fix API keys or (2) Add Ollama local AI first? Enter 1 or 2: "

if "%choice%"=="1" (
    echo.
    echo Please get your API keys from the URLs above, then run:
    echo   update-api-keys.bat
) else if "%choice%"=="2" (
    echo.
    echo Great choice! Installing Ollama local AI...
    call install-ollama.bat
) else (
    echo Invalid choice. Please run this script again.
)

pause
