# 🚀 AI Terminal with Local LLM (Ollama + Gemma2)

## Quick Setup Guide

### What You Need
- Ollama (free, open-source LLM runner)
- A local model like Gemma2 (free)
- This modified `ai-terminal-local.py` script

---

## Step 1: Install Ollama

### For Arch Linux:

```bash
# Using yay (AUR helper)
yay -S ollama

# Or manually
curl -fsSL https://ollama.ai/install.sh | sh
```

### Verify Installation:
```bash
ollama --version
```

---

## Step 2: Pull a Model

### Option A: Gemma2 (Recommended - Fast & Good Quality)
```bash
ollama pull gemma2
```

### Other Popular Models:
```bash
ollama pull llama2          # Meta's Llama 2 (7B - solid)
ollama pull mistral         # Mistral 7B (fast & good)
ollama pull neural-chat     # Intel's Neural Chat (good for tasks)
ollama pull orca-mini       # Small, capable model
```

**Size Guide:**
- Gemma2: ~5.5 GB
- Llama2: ~3.8 GB  
- Mistral: ~4.1 GB
- Orca-mini: ~1.7 GB

---

## Step 3: Start Ollama Server

```bash
# Start Ollama in background
ollama serve

# Or in a separate terminal, then come back to this one
```

You should see:
```
Starting Ollama
```

The server runs on `http://localhost:11434` by default.

---

## Step 4: Install AI Terminal (Local Version)

```bash
# Copy the local version
cp ai-terminal-local.py ~/.local/bin/ai-terminal
chmod +x ~/.local/bin/ai-terminal
```

---

## Step 5: Configure

The configuration is automatically created at `~/.ai_terminal_config`:

```json
{
  "backend": "local",
  "model": "gemma4:latest",
  "ollama_host": "http://localhost:11434",
  "auto_execute": false,
  "show_reasoning": true,
  "history_enabled": true
}
```

### To Change Model:

```bash
# Edit the config
nano ~/.ai_terminal_config

# Change "model": "gemma2" to "model": "llama2" (or any other)
```

Or after launching:
```bash
AI$ config
# Then edit ~/.ai_terminal_config and restart
```

---

## Step 6: Launch!

```bash
ai-terminal
```

You should see:
```
╔════════════════════════════════════════╗
║   🤖 AI-Powered Terminal (Arch Linux)   ║
║   Backend: LOCAL                        ║
║   Model: GEMMA2                         ║
║   Type 'help' for commands              ║
╚════════════════════════════════════════╝
```

---

## 💡 Usage

### Try These Commands:

```
AI$ show all Python files in this directory
AI$ find files larger than 100MB
AI$ count lines of code
AI$ check disk usage
AI$ ? How do I use grep?
AI$ models
AI$ backend
```

### New Commands Available:

- **`models`** - List all Ollama models installed
- **`backend`** - Show which backend you're using (local or anthropic)

---

## ⚙️ Advanced Configuration

### Switch Between Local and Cloud:

Edit `~/.ai_terminal_config`:

```json
{
  "backend": "local",
  "model": "gemma4:latest"
}
```

Or:

```json
{
  "backend": "anthropic",
  "model": "claude-opus-4-6"
}
```

**Note:** For Anthropic, you still need `ANTHROPIC_API_KEY` set.

### Change Ollama Host:

If you're running Ollama on a different machine:

```json
{
  "ollama_host": "http://192.168.1.100:11434"
}
```

---

## 🐛 Troubleshooting

### "Cannot connect to Ollama at http://localhost:11434"

**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# In a new terminal, verify it's up
curl http://localhost:11434/api/tags
```

### "Model not found: gemma2"

**Solution:**
```bash
# Pull the model
ollama pull gemma2

# List available models
ollama list
```

### "Request timed out"

**Solution:**
- Model is loading or processing (wait)
- Your system might be slow (use smaller model like `orca-mini`)
- Ollama server crashed (restart with `ollama serve`)

### "Permission denied"

**Solution:**
```bash
chmod +x ~/.local/bin/ai-terminal
```

---

## 📊 Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **Gemma2** | 5.5 GB | Fast | Excellent | ✅ Best overall |
| **Llama2** | 3.8 GB | Medium | Good | General tasks |
| **Mistral** | 4.1 GB | Fast | Very Good | Speed + quality |
| **Orca-mini** | 1.7 GB | Very Fast | Fair | Low-end systems |

**Recommendation:** Start with **Gemma2** for the best balance.

---

## 🚀 Performance Tips

### 1. Use GPU Acceleration

If your system has NVIDIA GPU:

```bash
# Install CUDA support (if you have NVIDIA GPU)
# Ollama will use GPU automatically if available
```

For AMD GPU:
```bash
# Ollama detects AMD ROCm automatically
```

### 2. Optimize Model Selection

For faster responses on slow systems:
```bash
ollama pull orca-mini  # Only 1.7 GB
```

### 3. Pre-load Model

Keep model in memory to avoid loading delay:
```bash
# Run a test command to keep model loaded
ollama run gemma2 "hello"
```

---

## 🔄 Switching Between Backends

### Use Local When:
✅ You want privacy (no cloud upload)
✅ You want offline usage
✅ You don't want to pay per API call
✅ You have powerful local hardware
✅ You want complete control

### Use Anthropic When:
✅ You want the best quality (Claude 3.5 Sonnet)
✅ You want the latest models
✅ You prefer cloud-based updates
✅ You have low local resources
✅ You don't mind paying per API call

---

## 📝 Configuration Examples

### Minimal Config (Fast)
```json
{
  "backend": "local",
  "model": "orca-mini",
  "ollama_host": "http://localhost:11434",
  "auto_execute": false,
  "show_reasoning": false,
  "history_enabled": false
}
```

### Full Config (Safe)
```json
{
  "backend": "local",
  "model": "gemma4:latest",
  "ollama_host": "http://localhost:11434",
  "auto_execute": false,
  "show_reasoning": true,
  "history_enabled": true
}
```

### Power User Config (Fast Execution)
```json
{
  "backend": "local",
  "model": "mistral",
  "ollama_host": "http://localhost:11434",
  "auto_execute": true,
  "show_reasoning": false,
  "history_enabled": true
}
```

---

## 💻 Typical Workflow

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start AI Terminal
ai-terminal

# In AI Terminal:
AI$ show Python files
🤖 Thinking...        # Ollama processing locally
Command generated
find . -type f -name "*.py"

Execute? (y/n/e): y
[Results...]
```

---

## 🎓 Learning the Models

The AI Terminal uses your local models to:
1. Understand your natural language request
2. Generate proper bash syntax
3. Run the command with your confirmation
4. Track everything in history

All processing happens **on your machine** - nothing leaves your computer!

---

## 📊 System Requirements

### Minimum:
- CPU: Modern dual-core
- RAM: 8 GB
- Storage: 6-10 GB for model

### Recommended:
- CPU: Modern quad-core+
- RAM: 16 GB+
- Storage: 20 GB for multiple models
- GPU: Optional but speeds up significantly

---

## 🔗 Useful Links

- **Ollama:** https://ollama.ai
- **Ollama Models:** https://ollama.ai/library
- **Gemma2:** https://ollama.ai/library/gemma2
- **API Docs:** https://github.com/ollama/ollama/blob/main/docs/api.md

---

## 💡 Pro Tips

### 1. Create a Script to Auto-Start Ollama

Create `~/start-ai-terminal.sh`:
```bash
#!/bin/bash
# Start Ollama in background
ollama serve &
sleep 2
# Wait for it to start, then launch AI terminal
ai-terminal
```

Make it executable:
```bash
chmod +x ~/start-ai-terminal.sh
```

### 2. Keep Model Loaded

Add to your `.bashrc` or `.zshrc`:
```bash
# Pre-load Gemma2 on startup (optional)
# ollama run gemma2 "hello" &> /dev/null &
```

### 3. Monitor Ollama

```bash
# Check if Ollama is running
ps aux | grep ollama

# Kill Ollama if stuck
pkill -f "ollama serve"

# Start fresh
ollama serve
```

---

## 🆚 Local vs Cloud Comparison

| Feature | Local | Cloud |
|---------|-------|-------|
| **Privacy** | ✅ Full | ❌ Shared |
| **Cost** | ✅ Free | ⚠️ Pay per use |
| **Quality** | ⚠️ Good | ✅ Excellent |
| **Offline** | ✅ Yes | ❌ No |
| **Speed** | ⚠️ Variable | ✅ Fast |
| **Updates** | ❌ Manual | ✅ Auto |

---

## 🚀 You're All Set!

Start using your local AI terminal:

```bash
# Make sure Ollama is running
ollama serve

# In another terminal
ai-terminal

# Try a command
AI$ list recent files
```

**No internet required. No API keys. Just pure local AI power!** 💪

---

## Next Steps

1. Install Ollama
2. Pull Gemma2: `ollama pull gemma2`
3. Start server: `ollama serve`
4. Setup AI Terminal (local version)
5. Launch and explore!

**Enjoy your private AI terminal!** 🎉
