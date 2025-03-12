#!/bin/bash
# Waze Home CLI Installation Script

# Exit on error
set -e

echo "=== Waze Home CLI Installer ==="
echo "This script will install the Waze Home CLI tool."

# Check if Python 3.10+ is installed
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        echo "Error: Python 3.10 or higher is required. Found Python $PYTHON_VERSION"
        exit 1
    fi
    
    echo "Found Python $PYTHON_VERSION"
    PYTHON_CMD="python3"
else
    echo "Error: Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install the package
echo "Installing Waze Home CLI..."
pip install -e .

# Verify installation
echo "Verifying installation..."
if command -v waze-home >/dev/null 2>&1; then
    echo "✅ Installation successful!"
    echo ""
    echo "You can now use the 'waze-home' command while the virtual environment is active."
    echo "To activate the virtual environment in the future, run:"
    echo "  source venv/bin/activate"
    echo ""
    echo "Try running 'waze-home --help' to see available commands."
else
    echo "❌ Installation failed. The 'waze-home' command was not found."
    exit 1
fi 