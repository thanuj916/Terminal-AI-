#!/bin/bash
# Ollama Diagnostic Tool
# Run this to check if everything is set up correctly

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Ollama & AI Terminal Diagnostic      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Ollama Installation
echo -e "${YELLOW}[1/6] Checking Ollama Installation...${NC}"
if command -v ollama &> /dev/null; then
    version=$(ollama --version)
    echo -e "${GREEN}✓ Ollama installed: $version${NC}"
else
    echo -e "${RED}✗ Ollama NOT installed${NC}"
    echo "   Install with: yay -S ollama"
    echo "   Or: https://ollama.ai"
fi
echo ""

# Test 2: Ollama Process
echo -e "${YELLOW}[2/6] Checking if Ollama is Running...${NC}"
if ps aux | grep -v grep | grep "ollama serve" > /dev/null; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
    ollama_running=true
else
    echo -e "${RED}✗ Ollama is NOT running${NC}"
    echo "   Start with: ollama serve"
    ollama_running=false
fi
echo ""

# Test 3: API Connection
echo -e "${YELLOW}[3/6] Testing Ollama API Connection...${NC}"
if [ "$ollama_running" = true ]; then
    if curl -s -m 2 http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ollama API is responding${NC}"
        api_working=true
    else
        echo -e "${RED}✗ Ollama API not responding${NC}"
        echo "   API should be at: http://localhost:11434"
        api_working=false
    fi
else
    echo -e "${RED}⊘ Skipped (Ollama not running)${NC}"
    api_working=false
fi
echo ""

# Test 4: Models
echo -e "${YELLOW}[4/6] Checking Installed Models...${NC}"
if [ "$ollama_running" = true ]; then
    models=$(ollama list 2>/dev/null | wc -l)
    if [ $models -gt 1 ]; then
        echo -e "${GREEN}✓ Models installed:${NC}"
        ollama list | tail -n +2 | awk '{print "   - " $1 " (" $2 ")"}'
    else
        echo -e "${RED}✗ No models installed${NC}"
        echo "   Install with: ollama pull gemma2"
    fi
else
    echo -e "${RED}⊘ Skipped (Ollama not running)${NC}"
fi
echo ""

# Test 5: AI Terminal
echo -e "${YELLOW}[5/6] Checking AI Terminal Installation...${NC}"
if [ -f ~/.local/bin/ai-terminal ]; then
    echo -e "${GREEN}✓ AI Terminal script found${NC}"
    if [ -x ~/.local/bin/ai-terminal ]; then
        echo -e "${GREEN}✓ AI Terminal is executable${NC}"
    else
        echo -e "${YELLOW}⚠ AI Terminal not executable${NC}"
        echo "   Fix with: chmod +x ~/.local/bin/ai-terminal"
    fi
else
    echo -e "${RED}✗ AI Terminal NOT installed${NC}"
    echo "   Copy ai-terminal-local.py to ~/.local/bin/ai-terminal"
fi
echo ""

# Test 6: Configuration
echo -e "${YELLOW}[6/6] Checking AI Terminal Configuration...${NC}"
if [ -f ~/.ai_terminal_config ]; then
    echo -e "${GREEN}✓ Config file found${NC}"
    backend=$(grep '"backend"' ~/.ai_terminal_config | grep -o '"[^"]*"$' | tr -d '"')
    model=$(grep '"model"' ~/.ai_terminal_config | grep -o '"[^"]*"$' | tr -d '"')
    echo "   Backend: $backend"
    echo "   Model: $model"
    
    if [ "$backend" = "local" ]; then
        echo -e "${GREEN}✓ Configured for LOCAL backend${NC}"
    fi
else
    echo -e "${YELLOW}⚠ No config file (will be created on first run)${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          SUMMARY & NEXT STEPS          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

if [ "$api_working" = true ]; then
    echo -e "${GREEN}✅ Everything looks good!${NC}"
    echo ""
    echo "Try these commands:"
    echo -e "${YELLOW}  ai-terminal${NC}"
    echo ""
    echo "Then in the AI terminal:"
    echo -e "${YELLOW}  AI$ show Python files${NC}"
    echo ""
else
    echo -e "${RED}❌ Issues found. Fix them:${NC}"
    echo ""
    
    if [ "$ollama_running" = false ]; then
        echo "1. Start Ollama:"
        echo -e "${YELLOW}   ollama serve${NC}"
    fi
    
    if [ "$api_working" = false ]; then
        echo "2. Make sure Ollama API is responding:"
        echo -e "${YELLOW}   curl http://localhost:11434/api/tags${NC}"
    fi
    
    models=$(ollama list 2>/dev/null | wc -l)
    if [ "$ollama_running" = true ] && [ $models -le 1 ]; then
        echo "3. Pull a model:"
        echo -e "${YELLOW}   ollama pull gemma2${NC}"
    fi
    
    echo ""
    echo "Then run this diagnostic again to verify."
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""
