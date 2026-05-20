# ⚡ QUICK FIX: Ollama 404 Error

## You're getting this error:
```
❌ Ollama API not found (404)
```

## 5-Minute Fix

### Step 1: Check Ollama is Running

```bash
# In one terminal, check if Ollama is running
ps aux | grep ollama
```

**If NOT showing `ollama serve`:**
```bash
# Start Ollama in a new terminal
ollama serve

# Wait for it to say "Starting Ollama"
# LEAVE THIS TERMINAL OPEN
```

### Step 2: Verify Ollama API Works

**In a DIFFERENT terminal:**

```bash
# Test the API
curl http://localhost:11434/api/tags
```

**Should show:** JSON with your models list (like `{"models":[...]}`)

**If you get "Connection refused":**
- Go back to Step 1 and make sure `ollama serve` is running
- Check that it's actually printed "Starting Ollama"

**If you get "404" or similar:**
- Restart Ollama: Kill it and run `ollama serve` again

### Step 3: Make Sure You Have a Model

```bash
# List your models
ollama list

# Should show at least one, like:
# gemma2:latest    5.5 GB
```

**If empty or no model:**
```bash
# Pull Gemma2 (or another model)
ollama pull gemma2

# Wait for download to finish (5-20 minutes)
```

### Step 4: Restart AI Terminal

```bash
# Kill the old AI terminal
ai-terminal
# (Press Ctrl+C)

# Start fresh
ai-terminal
```

### Step 5: Try a Command

```bash
AI$ show me Python files
```

---

## Detailed Checklist

Copy-paste this to verify each step:

```bash
# 1. Is Ollama running?
ps aux | grep "ollama serve"

# 2. Is API responding?
curl http://localhost:11434/api/tags

# 3. Do you have models?
ollama list

# 4. Can you run a model directly?
ollama run gemma2 "hello"

# 5. Does config have right backend?
grep "backend" ~/.ai_terminal_config

# 6. Does config have right model?
grep "model" ~/.ai_terminal_config
```

All should show success ✓

---

## Most Common Causes (In Order)

1. **Ollama not running** (80% of cases)
   - **Fix:** Run `ollama serve` in a terminal and keep it open

2. **Wrong model name in config** (10% of cases)
   - **Fix:** Check `ollama list` and update `~/.ai_terminal_config`

3. **No model downloaded** (7% of cases)
   - **Fix:** Run `ollama pull gemma2`

4. **Ollama server crashed** (3% of cases)
   - **Fix:** Kill Ollama and restart: `pkill -f ollama serve` then `ollama serve`

---

## The 2-Terminal Setup (Correct Way)

### Terminal 1: Keep Ollama Running
```bash
ollama serve
# This stays open forever
# You'll see: "Starting Ollama"
# No errors = it's working
```

### Terminal 2: Use AI Terminal
```bash
ai-terminal
# Use normally
```

**Never close Terminal 1** - AI Terminal needs it running!

---

## Diagnostic Tool

Run this to diagnose everything:

```bash
bash diagnose-ollama.sh
```

It will tell you exactly what's wrong.

---

## Still Not Working?

### Run this full diagnostic:

```bash
echo "=== Ollama Status ==="
ps aux | grep ollama

echo "=== API Test ==="
curl -v http://localhost:11434/api/tags

echo "=== Models ==="
ollama list

echo "=== Config ==="
cat ~/.ai_terminal_config

echo "=== AI Terminal ==="
which ai-terminal
```

Copy the output and we can debug specifically.

---

## Nuclear Option: Complete Reset

```bash
# 1. Kill everything
pkill -f ollama
sleep 2
pkill -f ai-terminal
sleep 2

# 2. Reset config
rm ~/.ai_terminal_config

# 3. Restart Ollama
ollama serve

# 4. In new terminal, verify
ollama list
ollama run gemma2 "test"

# 5. Try AI terminal
ai-terminal
```

---

## The Key Point

**Ollama MUST be running in a terminal while you use AI Terminal.**

```
Terminal 1 (Always Running):
  $ ollama serve
  Starting Ollama
  [stays here forever]

Terminal 2 (Use for AI):
  $ ai-terminal
  🤖 AI-Powered Terminal
  AI$ [your commands here]
```

If you close Terminal 1, AI Terminal stops working!

---

## Quick Test

```bash
# Terminal 1
ollama serve

# Terminal 2 (new terminal)
ollama list          # Should show models
ollama run gemma2 "hi"  # Should respond
ai-terminal          # Should work
```

---

## Common Messages & Fixes

| Message | Cause | Fix |
|---------|-------|-----|
| "Connection refused" | Ollama not running | Run `ollama serve` |
| "404 Not Found" | API endpoint wrong | Restart Ollama |
| "Cannot connect" | Wrong host/port | Check config |
| "Empty response" | Model not loaded | Run `ollama run gemma2` |
| "Timed out" | System slow/model busy | Wait or use faster model |

---

## That's It!

95% of the time it's just "Ollama not running"

```bash
ollama serve
# ← Keep this open
# → Use another terminal for ai-terminal
```

**Enjoy your working AI Terminal!** 🎉
