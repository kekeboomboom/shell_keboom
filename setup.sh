#!/bin/bash

echo "=== Model Success Order Rate Statistics Calculator Setup ==="
echo "Setting up the script on macOS..."

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Install dependencies
echo "Installing required dependencies..."
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas openpyxl

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x interactive_statistics.py

if [ $? -eq 0 ]; then
    echo "✓ Scripts are now executable"
else
    echo "✗ Failed to make scripts executable"
    exit 1
fi

# Test the script
echo "Testing script installation..."
python3 statistic_model_success_order_rate.py --help > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Script is working correctly"
else
    echo "✗ Script test failed"
    exit 1
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "🎯 Two ways to use the calculator:"
echo ""
echo "1. 🖱️  Interactive Mode (Recommended for beginners):"
echo "   python3 interactive_statistics.py"
echo ""
echo "2. 💻 Command Line Mode:"
echo "   python3 statistic_model_success_order_rate.py \\"
echo "     --base_data yilian_output.txt \\"
echo "     --need_statistic data.xlsx"
echo ""
echo "📚 For more information, see README_INSTALLATION.md"
echo "❓ For help: python3 statistic_model_success_order_rate.py --help" 
