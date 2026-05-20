#!/usr/bin/env python3
"""
AI-Powered Terminal Wrapper (Local LLM Support)
Converts natural language commands to shell commands using either:
1. Local LLM (Ollama - Gemma2, Llama2, Mistral, etc.)
2. Cloud-based Claude API (Anthropic)
"""

import subprocess
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import requests

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AITerminal:
    def __init__(self):
        self.history_file = Path.home() / ".ai_terminal_history"
        self.config_file = Path.home() / ".ai_terminal_config"
        self.load_config()
        self.detect_llm_backend()
        
    def load_config(self):
        """Load user configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "backend": "local",  # "local" or "anthropic"
                "model": "gemma2",   # local model name (gemma2, llama2, mistral, etc.)
                "ollama_host": "http://localhost:11434",  # Ollama server address
                "auto_execute": False,
                "show_reasoning": True,
                "history_enabled": True
            }
            self.save_config()
    
    def save_config(self):
        """Save user configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def detect_llm_backend(self):
        """Detect which LLM backend to use"""
        backend = self.config.get("backend", "local").lower()
        
        if backend == "local":
            self.llm_type = "local"
            if not self.check_ollama():
                print(f"{Colors.RED}❌ Ollama not running!{Colors.ENDC}")
                print(f"{Colors.YELLOW}Start Ollama with: ollama serve{Colors.ENDC}")
                print(f"{Colors.YELLOW}Or install from: https://ollama.ai{Colors.ENDC}\n")
                sys.exit(1)
        elif backend == "anthropic":
            self.llm_type = "anthropic"
            if not os.getenv("ANTHROPIC_API_KEY"):
                print(f"{Colors.RED}❌ ANTHROPIC_API_KEY not set!{Colors.ENDC}")
                sys.exit(1)
            try:
                import anthropic
                self.client = anthropic.Anthropic()
            except ImportError:
                print(f"{Colors.RED}❌ anthropic SDK not installed!{Colors.ENDC}")
                print(f"{Colors.YELLOW}Install with: pip3 install anthropic --user{Colors.ENDC}")
                sys.exit(1)
        else:
            print(f"{Colors.RED}Unknown backend: {backend}{Colors.ENDC}")
            sys.exit(1)
    
    def check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(
                f"{self.config['ollama_host']}/api/tags",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False
    
    def print_header(self):
        """Print welcome header"""
        backend = self.config.get("backend", "local")
        model = self.config.get("model", "unknown")
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}╔════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║   🤖 AI-Powered Terminal (Arch Linux)   ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║   Backend: {backend.upper():30} ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║   Model: {model.upper():33} ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}║   Type 'help' for commands              ║{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}╚════════════════════════════════════════╝{Colors.ENDC}\n")
    
    def print_help(self):
        """Print help information"""
        help_text = f"""
{Colors.BOLD}{Colors.CYAN}Available Commands:{Colors.ENDC}
  {Colors.GREEN}help{Colors.ENDC}           - Show this help message
  {Colors.GREEN}clear{Colors.ENDC}          - Clear the screen
  {Colors.GREEN}history{Colors.ENDC}        - Show command history
  {Colors.GREEN}config{Colors.ENDC}         - Show/edit configuration
  {Colors.GREEN}backend{Colors.ENDC}        - Show current backend
  {Colors.GREEN}models{Colors.ENDC}         - List available Ollama models (local only)
  {Colors.GREEN}exit{Colors.ENDC}           - Exit the terminal
  {Colors.GREEN}!!{Colors.ENDC}              - Execute last command directly in shell
  {Colors.GREEN}?{Colors.ENDC} <query>      - Ask a question (no command execution)

{Colors.BOLD}{Colors.CYAN}Usage Examples:{Colors.ENDC}
  {Colors.YELLOW}Show all Python files in current directory{Colors.ENDC}
  {Colors.YELLOW}List files larger than 100MB{Colors.ENDC}
  {Colors.YELLOW}Check disk usage of /home{Colors.ENDC}
  {Colors.YELLOW}Find recently modified files{Colors.ENDC}
  {Colors.YELLOW}Create a backup of my config folder{Colors.ENDC}

{Colors.BOLD}{Colors.CYAN}Tips:{Colors.ENDC}
  • Be specific and descriptive in your requests
  • Ask follow-up questions for clarification
  • Review the suggested command before executing
  • Use 'help' anytime you need assistance
  • Use 'backend' to see which LLM you're using
"""
        print(help_text)
    
    def ask_llm_anthropic(self, user_query: str, is_question: bool = False) -> tuple:
        """Use Anthropic Claude API"""
        if is_question:
            system_prompt = """You are a helpful Linux assistant. Answer the user's question about Linux, 
            terminal usage, or system administration. Provide clear, concise explanations."""
        else:
            system_prompt = """You are a Linux command generator. Convert natural language requests into accurate bash commands.

IMPORTANT RULES:
1. Return ONLY the bash command, nothing else
2. Use safe commands - avoid destructive operations without user confirmation
3. For file deletion/modification, use prompts like 'rm -i' for interactive mode
4. For potentially dangerous operations, prefix with a safety comment
5. Optimize for readability and best practices
6. If the request is ambiguous, provide the most common interpretation"""

        try:
            message = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_query}]
            )
            response_text = message.content[0].text.strip()
            return response_text, None
        except Exception as e:
            return None, f"API Error: {str(e)}"
    
    def ask_llm_local(self, user_query: str, is_question: bool = False) -> tuple:
        """Use local Ollama LLM (Gemma2, Llama2, Mistral, etc.)"""
        model = self.config.get("model", "gemma2")
        
        if is_question:
            system_prompt = """You are a helpful Linux assistant. Answer the user's question about Linux, 
terminal usage, or system administration. Provide clear, concise explanations."""
        else:
            system_prompt = """You are a Linux command generator. Convert natural language requests into accurate bash commands.

IMPORTANT RULES:
1. Return ONLY the bash command, nothing else
2. Use safe commands - avoid destructive operations without user confirmation
3. For file deletion/modification, use prompts like 'rm -i' for interactive mode
4. For potentially dangerous operations, prefix with a safety comment
5. Optimize for readability and best practices
6. If the request is ambiguous, provide the most common interpretation

Examples:
- User: "show me all Python files"
  Response: find . -type f -name "*.py"
- User: "check disk usage"
  Response: du -sh /*"""

        try:
            host = self.config.get('ollama_host', 'http://localhost:11434')
            
            # Try to use Ollama API
            api_url = f"{host}/api/generate"
            
            payload = {
                "model": model,
                "prompt": f"{system_prompt}\n\nUser: {user_query}\n\nAssistant:",
                "stream": False,
                "temperature": 0.3,
            }
            
            response = requests.post(
                api_url,
                json=payload,
                timeout=60,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 404:
                return None, f"❌ Ollama API not found (404). Try:\n  1. Make sure Ollama is running: ollama serve\n  2. Check Ollama is on {host}\n  3. Verify model exists: ollama list"
            elif response.status_code != 200:
                return None, f"Ollama Error: {response.status_code} - {response.text[:200]}"
            
            result = response.json()
            response_text = result.get("response", "").strip()
            
            if not response_text:
                return None, "Ollama returned empty response. Model might not be loaded."
            
            # Clean up response - remove system prompts or extra text
            lines = response_text.split('\n')
            # Take first line that looks like a command
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('User:', 'Assistant:', 'System:', 'The', 'You', 'I ')):
                    response_text = line
                    break
            
            return response_text, None
            
        except requests.exceptions.ConnectionError as e:
            return None, f"❌ Cannot connect to Ollama at {self.config['ollama_host']}\nMake sure it's running with: ollama serve"
        except requests.exceptions.Timeout:
            return None, "❌ Ollama request timed out. Model is busy or too slow."
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def ask_llm(self, user_query: str, is_question: bool = False) -> tuple:
        """Route to appropriate LLM backend"""
        if self.llm_type == "local":
            return self.ask_llm_local(user_query, is_question)
        else:
            return self.ask_llm_anthropic(user_query, is_question)
    
    def execute_command(self, command: str) -> tuple:
        """Execute a shell command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out (30 seconds)", 124
        except Exception as e:
            return "", f"Execution error: {str(e)}", 1
    
    def save_to_history(self, user_input: str, command: str, output: str, success: bool):
        """Save command to history"""
        if not self.config.get("history_enabled", True):
            return
        
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "command": command,
            "backend": self.config.get("backend", "local"),
            "model": self.config.get("model", "unknown"),
            "success": success,
            "output_length": len(output)
        }
        
        try:
            history = []
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            
            history.append(history_entry)
            history = history[-100:]  # Keep last 100
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"{Colors.RED}Warning: Could not save to history: {e}{Colors.ENDC}")
    
    def show_history(self):
        """Display command history"""
        if not self.history_file.exists():
            print(f"{Colors.YELLOW}No history yet{Colors.ENDC}")
            return
        
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}Command History (Last 20):{Colors.ENDC}")
            print(f"{Colors.CYAN}{'-' * 100}{Colors.ENDC}")
            
            for i, entry in enumerate(history[-20:], 1):
                timestamp = entry['timestamp'][:19]
                backend = entry.get('backend', 'unknown')
                model = entry.get('model', '?')
                user_input = entry['user_input'][:60]
                success = f"{Colors.GREEN}✓{Colors.ENDC}" if entry['success'] else f"{Colors.RED}✗{Colors.ENDC}"
                print(f"{i:2}. [{success}] {timestamp} | {backend}/{model:8} | {user_input}")
            
            print(f"{Colors.CYAN}{'-' * 100}{Colors.ENDC}\n")
        except Exception as e:
            print(f"{Colors.RED}Error reading history: {e}{Colors.ENDC}")
    
    def show_ollama_models(self):
        """Show available Ollama models"""
        if self.llm_type != "local":
            print(f"{Colors.YELLOW}Not using local backend{Colors.ENDC}")
            return
        
        try:
            response = requests.get(
                f"{self.config['ollama_host']}/api/tags",
                timeout=5
            )
            
            if response.status_code != 200:
                print(f"{Colors.RED}Cannot connect to Ollama{Colors.ENDC}")
                return
            
            models = response.json().get("models", [])
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}Available Models:{Colors.ENDC}")
            print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")
            
            current = self.config.get("model", "unknown")
            for model in models:
                name = model['name'].split(':')[0]
                size = model.get('size', 0)
                size_gb = size / (1024**3)
                marker = f" {Colors.GREEN}(current){Colors.ENDC}" if name == current else ""
                print(f"  {name:20} {size_gb:6.1f} GB{marker}")
            
            print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}\n")
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.ENDC}")
    
    def show_config(self):
        """Show current configuration"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}Current Configuration:{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}")
        
        backend = self.config.get("backend", "local")
        print(f"{Colors.GREEN}Backend{Colors.ENDC:20}: {backend}")
        
        if backend == "local":
            model = self.config.get("model", "gemma2")
            ollama_host = self.config.get("ollama_host", "http://localhost:11434")
            print(f"{Colors.GREEN}Model{Colors.ENDC:20}: {model}")
            print(f"{Colors.GREEN}Ollama Host{Colors.ENDC:20}: {ollama_host}")
        
        for key, value in self.config.items():
            if key not in ['backend', 'model', 'ollama_host']:
                print(f"{Colors.GREEN}{key:20}{Colors.ENDC}: {value}")
        
        print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}\n")
    
    def confirm_execution(self, command: str) -> bool:
        """Ask user to confirm command execution"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}Suggested command:{Colors.ENDC}")
        print(f"{Colors.YELLOW}{command}{Colors.ENDC}\n")
        
        while True:
            response = input(f"{Colors.BOLD}Execute? (y/n/e): {Colors.ENDC}").strip().lower()
            if response == 'y':
                return True
            elif response == 'n':
                return False
            elif response == 'e':
                edited = input(f"{Colors.BOLD}Edit command: {Colors.ENDC}")
                if edited:
                    return self.confirm_execution(edited)
                return False
            else:
                print("Please enter 'y' (yes), 'n' (no), or 'e' (edit)")
    
    def handle_special_commands(self, user_input: str) -> bool:
        """Handle special built-in commands. Returns True if handled."""
        user_input = user_input.strip().lower()
        
        if user_input == 'help':
            self.print_help()
            return True
        elif user_input == 'clear':
            os.system('clear')
            return True
        elif user_input == 'history':
            self.show_history()
            return True
        elif user_input == 'config':
            self.show_config()
            return True
        elif user_input == 'backend':
            print(f"\n{Colors.CYAN}Current Backend: {self.llm_type.upper()}{Colors.ENDC}")
            if self.llm_type == "local":
                print(f"{Colors.CYAN}Model: {self.config.get('model', 'gemma2')}{Colors.ENDC}\n")
            return True
        elif user_input == 'models':
            if self.llm_type == "local":
                self.show_ollama_models()
            else:
                print(f"{Colors.YELLOW}Models command only works with local backend{Colors.ENDC}\n")
            return True
        elif user_input == 'exit' or user_input == 'quit':
            print(f"\n{Colors.GREEN}Goodbye! 👋{Colors.ENDC}\n")
            sys.exit(0)
        elif user_input == '!!':
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
                    if history:
                        last_command = history[-1]['command']
                        print(f"{Colors.YELLOW}Executing: {last_command}{Colors.ENDC}")
                        stdout, stderr, code = self.execute_command(last_command)
                        if stdout:
                            print(stdout)
                        if stderr:
                            print(f"{Colors.RED}{stderr}{Colors.ENDC}")
                        return True
            print(f"{Colors.YELLOW}No previous command found{Colors.ENDC}")
            return True
        
        return False
    
    def run(self):
        """Main terminal loop"""
        self.print_header()
        self.print_help()
        
        try:
            while True:
                try:
                    user_input = input(f"{Colors.BOLD}{Colors.CYAN}AI$ {Colors.ENDC}").strip()
                    
                    if not user_input:
                        continue
                    
                    if self.handle_special_commands(user_input):
                        continue
                    
                    is_question = user_input.startswith('?')
                    if is_question:
                        user_input = user_input[1:].strip()
                    
                    print(f"{Colors.BLUE}🤖 Thinking...{Colors.ENDC}")
                    response, error = self.ask_llm(user_input, is_question=is_question)
                    
                    if error:
                        print(f"{Colors.RED}{error}{Colors.ENDC}")
                        continue
                    
                    if is_question:
                        print(f"\n{Colors.GREEN}Answer:{Colors.ENDC}")
                        print(response)
                        print()
                        continue
                    
                    if self.config.get("show_reasoning", True):
                        print(f"{Colors.BLUE}Command generated{Colors.ENDC}")
                    
                    if not self.config.get("auto_execute", False):
                        if not self.confirm_execution(response):
                            print(f"{Colors.YELLOW}Command cancelled{Colors.ENDC}\n")
                            continue
                    
                    print(f"{Colors.BLUE}Executing...{Colors.ENDC}\n")
                    stdout, stderr, code = self.execute_command(response)
                    
                    self.save_to_history(user_input, response, stdout + stderr, code == 0)
                    
                    if stdout:
                        print(stdout)
                    if stderr:
                        print(f"{Colors.RED}{stderr}{Colors.ENDC}")
                    
                    if code != 0:
                        print(f"{Colors.YELLOW}Exit code: {code}{Colors.ENDC}\n")
                    
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}Cancelled{Colors.ENDC}\n")
                    continue
        
        except Exception as e:
            print(f"{Colors.RED}Fatal error: {e}{Colors.ENDC}")
            sys.exit(1)


if __name__ == "__main__":
    terminal = AITerminal()
    terminal.run()
