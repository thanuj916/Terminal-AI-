#!/bin/bash
# Installation script for AI Terminal with Local LLM Support

set -e

echo "🚀 Installing AI-Powered Terminal with Local LLM Support..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Install it with: sudo pacman -S python"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed."
    echo "Install it with: sudo pacman -S python-pip"
    exit 1
fi

echo "✓ pip found"

# Install required packages
echo ""
echo "📦 Installing Python dependencies..."
#pip3 install requests --user
sudo pacman -S python-requests

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Choose your LLM backend:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1) LOCAL (Ollama + Gemma2) - Free, private, offline"
echo "2) CLOUD (Anthropic Claude) - Best quality, requires API key"
echo ""
read -p "Enter choice (1 or 2): " backend_choice

if [ "$backend_choice" == "1" ]; then
    echo ""
    echo "📝 Setting up LOCAL LLM backend (Ollama)..."
    
    # Copy local version
    mkdir -p ~/.local/bin
    cp ai-terminal-local.py ~/.local/bin/ai-terminal
    chmod +x ~/.local/bin/ai-terminal
    
    echo "✓ AI Terminal installed with LOCAL backend"
    
    # Check if Ollama is installed
    echo ""
    if command -v ollama &> /dev/null; then
        echo "✓ Ollama found: $(ollama --version)"
    else
        echo "⚠️  Ollama not installed yet"
        echo "Install with: yay -S ollama (AUR) or https://ollama.ai"
        echo ""
        read -p "Would you like to install Ollama now? (y/n): " install_ollama
        if [ "$install_ollama" == "y" ]; then
            echo "Note: Installation depends on your AUR helper (yay/paru)"
            echo "Run: yay -S ollama"
        fi
    fi
    
    # Check if models are available
    echo ""
    echo "📋 Checking Ollama models..."
    if command -v ollama &> /dev/null; then
        echo ""
        read -p "Would you like to pull a model now? (y/n): " pull_model
        if [ "$pull_model" == "y" ]; then
            echo ""
            echo "Available models:"
            echo "  gemma2 (5.5 GB) - Recommended"
            echo "  mistral (4.1 GB) - Fast"
            echo "  llama2 (3.8 GB) - Solid"
            echo "  orca-mini (1.7 GB) - Small"
            echo ""
            read -p "Enter model name (default: gemma2): " model_choice
            model_choice=${model_choice:-gemma2}
            
            echo "⏳ Pulling $model_choice... (this may take a while)"
            ollama pull "$model_choice"
            echo "✓ Model pulled successfully"
        fi
    fi

elif [ "$backend_choice" == "2" ]; then
    echo ""
    echo "📝 Setting up CLOUD backend (Anthropic Claude)..."
    
    # Copy cloud version
    mkdir -p ~/.local/bin
    cp ai-terminal.py ~/.local/bin/ai-terminal
    chmod +x ~/.local/bin/ai-terminal
    
    echo "✓ AI Terminal installed with CLOUD backend"
    
    # Install Anthropic SDK
    echo ""
    echo "📦 Installing Anthropic SDK..."
    pip3 install anthropic --user
    
    # Check if API key is set
    echo ""
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "⚠️  ANTHROPIC_API_KEY is not set"
        echo ""
        read -p "Enter your API key (or press Enter to skip): " api_key
        if [ ! -z "$api_key" ]; then
            ANTHROPIC_API_KEY="$api_key"
        fi
    else
        echo "✓ API key already set"
    fi
    
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        echo "✓ API key configured"
    else
        echo "ℹ️  You can set it later in your shell config"
    fi

else
    echo "❌ Invalid choice"
    exit 1
fi

# Setup shell configuration
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Configuring shell..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
    echo "✓ ~/.local/bin is already in PATH"
else
    echo "⚠️  ~/.local/bin is not in your PATH"
    echo "Add this to your shell config (~/.bashrc or ~/.zshrc):"
    echo ""
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo ""
    read -p "Add to ~/.bashrc now? (y/n): " add_path
    if [ "$add_path" == "y" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        echo "✓ Added to ~/.bashrc"
    fi
fi

# Set API key for cloud backend
if [ "$backend_choice" == "2" ] && [ ! -z "$ANTHROPIC_API_KEY" ]; then
    read -p "Add API key to ~/.bashrc? (y/n): " add_key
    if [ "$add_key" == "y" ]; then
        echo "export ANTHROPIC_API_KEY='$ANTHROPIC_API_KEY'" >> ~/.bashrc
        echo "✓ API key added to ~/.bashrc"
    fi
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     ✅ Installation Complete!          ║"
echo "╚════════════════════════════════════════╝"
echo ""

if [ "$backend_choice" == "1" ]; then
    echo "🎯 Next steps for LOCAL backend:"
    echo "  1. Start Ollama: ollama serve"
    echo "  2. In another terminal: ai-terminal"
    echo ""
else
    echo "🎯 Next steps for CLOUD backend:"
    echo "  1. Reload shell: source ~/.bashrc"
    echo "  2. Launch: ai-terminal"
    echo ""
fi

echo "📖 Setup guide: Read LOCAL_LLM_SETUP.md for detailed instructions"
echo ""
echo "Happy coding! 🚀"
