#!/usr/bin/env bash
set -u

echo ""
echo "============================================"
echo "Creative Studio MCP - Mac and Linux Installer"
echo "============================================"
echo ""
echo "This installer will:"
echo "1. Check Python"
echo "2. Create a local workspace"
echo "3. Install required software"
echo "4. Create your .env file"
echo "5. Test the server startup"
echo ""

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 was not found."
    echo ""
    echo "Install Python from:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "On Mac, you can also use:"
    echo "brew install python"
    echo ""
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt was not found."
    echo "Make sure install.sh is inside the creative-studio-mcp folder."
    echo ""
    exit 1
fi

echo "[1/5] Creating local workspace..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not create the local workspace."
        echo "Try reinstalling Python and make sure venv is available."
        echo ""
        exit 1
    fi
else
    echo "Local workspace already exists."
fi
echo "Done."
echo ""

echo "[2/5] Activating local workspace..."
. .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Could not activate the local workspace."
    echo ""
    exit 1
fi
echo "Done."
echo ""

echo "[3/5] Installing required software..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Could not install required software."
    echo "Check your internet connection and try again."
    echo ""
    exit 1
fi
echo "Done."
echo ""

echo "[4/5] Creating environment file..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << EOF
OPENAI_API_KEY=your_api_key_here
MCP_SERVER_NAME=creative-studio
MCP_SERVER_PATH=$(pwd)
EOF
    fi
    echo "Created .env."
else
    echo ".env already exists."
fi
echo ""

echo "[5/5] Testing server startup..."
python -m py_compile server.py
if [ $? -ne 0 ]; then
    echo "ERROR: server.py has a syntax problem."
    echo "Please check the error above."
    echo ""
    exit 1
fi
echo "Server file looks good."
echo ""

echo "============================================"
echo "Installation complete"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Open .env and add your API key if you plan to use API features."
echo "2. Run this command to test the server:"
echo "   .venv/bin/python server.py"
echo "3. Read QUICK_START.md for Claude or ChatGPT setup."
echo ""
