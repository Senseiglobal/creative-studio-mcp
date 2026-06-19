#!/bin/bash
# Creative Studio MCP - One-Click Installation (Mac/Linux)
# This script sets up everything needed to run the project

echo ""
echo "============================================"
echo "Creative Studio MCP - Installation"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo ""
    echo "Please install Python from: https://www.python.org/downloads/"
    echo "Or use: brew install python3 (on Mac)"
    echo ""
    exit 1
fi

echo "[1/4] Creating workspace..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi
echo "✓ Workspace created"

echo ""
echo "[2/4] Activating workspace..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "✓ Workspace activated"

echo ""
echo "[3/4] Installing software..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi
echo "✓ Software installed"

echo ""
echo "[4/4] Creating environment file..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Creative Studio MCP Configuration
# Get your OpenAI API Key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_api_key_here

# Server Configuration
MCP_SERVER_NAME=creative-studio
MCP_SERVER_PATH=$(pwd)
EOF
    echo "✓ Environment file created (.env)"
else
    echo "✓ Environment file already exists"
fi

echo ""
echo "============================================"
echo "✓ Installation Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Open .env file and add your OpenAI API Key"
echo "2. Read QUICK_START.md for next steps"
echo "3. Run: python server.py (to test)"
echo ""
