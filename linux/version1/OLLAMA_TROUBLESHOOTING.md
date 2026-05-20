# 🐛 Fixing Ollama 404 Error - Troubleshooting Guide

## The Problem
```
❌ Ollama API not found (404)
```

This means the AI Terminal can't connect to Ollama's API. Let's fix it!

---

## ✅ Quick Fix Checklist

### 1. **Is Ollama Actually Running?**

```bash
# Check if Ollama process is running
ps aux | grep ollama

# Should show something like:
# user      1234  0.0  0.1 ...ollama serve
```

**If NOT running:**
```bash
# Start Ollama in a separate terminal
ollama serve

# Should show:
# Starting Ollama
```

### 2. **Is the API Responding?**

```bash
# Test if Ollama API is working
curl http://localhost:11434/api/tags

# Should return JSON with your models list
```

**If you get "connection refused":**
- Ollama is not running → Run `ollama serve`
- Running on different port → Check config

**If you get "404 Not Found":**
- Ollama server issue → Restart it
- Check if Ollama version is updated

### 3. **Do You Have a Model Pulled?**

```bash
# List installed models
ollama list

# Should show at least one, like:
# gemma2:latest    5.5 GB
```

**If no models:**
```bash
# Pull Gemma2
ollama pull gemma2

# Wait for download to complete
```

### 4. **Is the Model Name Correct in Config?**

```bash
# Check your config
cat ~/.ai_terminal_config

# Look for "model" line - should match what's in ollama list
# "model": "gemma2"
```

---

## 🔧 Complete Troubleshooting Steps

### Step 1: Verify Ollama is Installed

```bash
which ollama
ollama --version

# If not found, install:
# yay -S ollama
```

### Step 2: Start Ollama Fresh

```bash
# Kill any existing Ollama process
pkill -f "ollama serve"
sleep 2

# Start fresh
ollama serve

# You should see:
# Starting Ollama
# (no errors)
```

### Step 3: Test Ollama API

**In a NEW terminal:**

```bash
# Test basic connection
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma2","prompt":"hello","stream":false}'

# Should return JSON with response field
```

**If this works, Ollama is fine. Problem is in ai-terminal config.**

### Step 4: Check AI Terminal Config

```bash
cat ~/.ai_terminal_config

# Should look like:
{
  "backend": "local",
  "model": "gemma2",
  "ollama_host": "http://localhost:11434",
  ...
}
```

### Step 5: Verify Model is Loaded

```bash
# List all models
ollama list

# Run a test to ensure it's loaded
ollama run gemma2 "hello"

# Wait for response, then it's working
```

---

## 🚨 Common Issues & Solutions

### Issue: "Cannot connect to Ollama"
**Cause:** Ollama not running or wrong host
**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# Check config has correct host
cat ~/.ai_terminal_config
# Should be: "ollama_host": "http://localhost:11434"
```

### Issue: "404 Not Found"
**Cause:** Ollama server responding but API endpoint wrong
**Solution:**
```bash
# Verify Ollama API works
curl http://localhost:11434/api/tags

# If 404, restart Ollama
pkill -f "ollama serve"
sleep 2
ollama serve
```

### Issue: "Empty response from Ollama"
**Cause:** Model not fully loaded or crashed
**Solution:**
```bash
# Check if model exists
ollama list

# If exists, reload it
ollama run gemma2

# Wait for it to load, then exit
# (Press Ctrl+D)

# Try AI terminal again
ai-terminal
```

### Issue: "Request timed out"
**Cause:** Model is slow or system is busy
**Solution:**
```bash
# Use a faster model
ollama pull mistral  # Faster than Gemma2
# or
ollama pull orca-mini  # Smaller/faster

# Update config
nano ~/.ai_terminal_config
# Change: "model": "mistral"

# Restart ai-terminal
```

---

## 🔍 Debug Mode: Test Everything

Create a test script to verify everything works:

```bash
#!/bin/bash
echo "Testing Ollama Setup..."

echo "1. Checking Ollama installation..."
which ollama && echo "✓ Ollama found" || echo "✗ Ollama NOT installed"

echo "2. Checking Ollama process..."
ps aux | grep -v grep | grep "ollama serve" && echo "✓ Ollama running" || echo "✗ Ollama NOT running"

echo "3. Testing API connection..."
curl -s http://localhost:11434/api/tags > /dev/null && echo "✓ API responding" || echo "✗ API not responding"

echo "4. Listing models..."
ollama list

echo "5. Testing model..."
echo "Testing with gemma2..."
ollama run gemma2 "say hello in one word"

echo "All tests done!"
```

Save as `test-ollama.sh`, then:
```bash
bash test-ollama.sh
```

---

## 🏥 Nuclear Option: Complete Reset

If nothing works, do a complete reset:

```bash
# 1. Kill Ollama
pkill -f "ollama"
sleep 2

# 2. Remove config
rm ~/.ai_terminal_config

# 3. Start fresh
ollama serve

# 4. In new terminal, pull model
ollama pull gemma2

# 5. Restart ai-terminal
ai-terminal
```

---

## 📋 Verification Checklist

Before trying AI Terminal, verify:

- [ ] `ollama --version` returns version
- [ ] `ps aux | grep ollama` shows running process
- [ ] `curl http://localhost:11434/api/tags` returns JSON
- [ ] `ollama list` shows at least one model
- [ ] `ollama run gemma2 "test"` produces output
- [ ] `cat ~/.ai_terminal_config` shows correct config
- [ ] `ai-terminal` launches without errors

---

## 🆘 Still Stuck? Try This

### Check Ollama Logs

```bash
# Ollama logs are usually in:
journalctl -u ollama  # If installed as service

# Or just watch output when running:
ollama serve
# Look for any error messages
```

### Check Your System

```bash
# Available memory
free -h

# Disk space
df -h

# CPU usage
top
```

**Requirements:**
- RAM: At least 8GB free
- Storage: At least 6GB free for model
- CPU: Any modern CPU works

### Reinstall Ollama

```bash
# Remove and reinstall
yay -R ollama
yay -S ollama

# Start fresh
ollama serve
ollama pull gemma2
```

---

## ✅ Success Indicators

When everything is working:

1. **Ollama Running:**
   ```
   $ ollama serve
   Starting Ollama
   [server continues running]
   ```

2. **API Responding:**
   ```
   $ curl http://localhost:11434/api/tags
   {"models":[{"name":"gemma2:latest",...}]}
   ```

3. **AI Terminal Starting:**
   ```
   $ ai-terminal
   🤖 AI-Powered Terminal (Arch Linux)
   Backend: LOCAL
   Model: GEMMA2
   ```

4. **Command Working:**
   ```
   AI$ show Python files
   🤖 Thinking...
   find . -type f -name "*.py"
   Execute? (y/n/e): y
   [Results...]
   ```

---

## 📞 Getting Help

**Share this info when asking for help:**

```bash
# Your system info
uname -a
ollama --version
ollama list

# Your config
cat ~/.ai_terminal_config

# Error message (full output)
# Copy the exact error you see
```

---

## 🎯 Next Steps

Once everything is working:

1. Read `LOCAL_QUICK_START.txt`
2. Try example commands
3. Check `LOCAL_LLM_SETUP.md` for advanced options
4. Enjoy your private AI terminal!

---

**You've got this!** 💪 The issue is usually just Ollama not running or wrong model name.
