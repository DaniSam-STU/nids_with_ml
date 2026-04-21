#!/bin/bash

echo "========================================"
echo "🚀 NIDS Project - One Click Installer"
echo "========================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "✅ Python detected"
echo ""

# Run launcher
echo "Starting setup..."
python3 launch.py