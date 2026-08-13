<div align="center">

```text
  __  __              ___   _       ___ 
 |  \/  |  __ _   ___| \ \ | |     |_ _|
 | |\/| | / _` | / __| |\ \| |      | | 
 | |  | || (_| || (__| | \ \ |___   | | 
 |_|  |_| \__,_| \___|_|  \_\____| |___|
          S W A R M   D I R E C T O R
            Crafted by Roedy Rustam
```
*A Cyberpunk-Inspired Neural Uplink for AI Swarm Orchestration*

</div>
A lightweight, beginner-friendly Python Command Line Interface (CLI) for orchestrating multiple AI agents. Built with **LiteLLM**, **Typer**, and **Rich**, this tool makes it incredibly easy to experiment with multi-agent workflows using any LLM provider (OpenAI, Anthropic, Gemini, Groq, xAI/Grok, DeepSeek, Ollama, etc.)—even on free tiers!

This project features native integration with the **Vibes-Plug** ecosystem, allowing agents to automatically learn new "skills" from simple Markdown files.

## ✨ Features
- **Multi-Provider Support**: Switch between Gemini, LLaMA (via Groq), Claude, GPT, Grok, or DeepSeek models effortlessly using `LiteLLM`.
- **Markdown Skill Injection**: Define expert skills in Markdown (`skills/` directory) and they will be automatically injected into your agent's system prompt.
- **Beautiful Terminal UI**: Uses `Rich` for gorgeous tables, colors, and loading animations.
- **YAML Configuration**: Easily define your agents, their roles, and step-by-step workflows in `agents.yaml`.
- **Beginner Friendly**: No heavy abstractions like LangGraph or AutoGen—just pure, transparent Python code that is easy to study and modify.

---

## 🛠️ Installation

### 🚀 Quick Install (Windows)

**Using PowerShell:**
```powershell
irm https://raw.githubusercontent.com/roedyrustam/multi_agent_cli/main/install.ps1 | iex
```

**Using CMD (requires curl):**
```cmd
curl -sSL https://raw.githubusercontent.com/roedyrustam/multi_agent_cli/main/install.bat -o install.bat && install.bat
```

*(Note: Don't forget to replace `YOUR_USERNAME` with your actual GitHub username before sharing these links!)*

### 🐳 Using Docker (Recommended)
If you have Docker and Docker Compose installed, you can skip Python environment setup entirely!
```bash
# Ensure you have your .env file ready
docker-compose up -d

# To attach to the interactive chat session:
docker attach multi_agent_cli_cli_1
```

### 🔧 Manual Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/roedyrustam/multi_agent_cli.git
   cd multi-agent-cli
   ```

2. **Create a virtual environment & Install**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   
   pip install -e .
   ```


4. **Set up Environment Variables & Default Model**
   The application comes with an interactive setup wizard! Simply run the setup command to configure your API keys and your `DEFAULT_MODEL` (e.g., `gemini/gemini-2.5-flash`, `xai/grok-beta`, or `deepseek/deepseek-chat`):
   ```bash
   macli setup
   ```
   Or you can manually rename `.env.example` to `.env` and add them yourself.

---

## 🚀 Usage

### 1. View all Commands
```bash
macli --help
```

### 2. View all Available Agents
```bash
macli list-agents
```

### 3. Check Available Skills
List all skills currently loaded in your `skills/` directory:
```bash
macli list-skills
```

### 4. Autonomous Swarm Director (Advanced)
Turn the CLI into a dynamic Swarm (like OpenDevin or Hermes). The Swarm Director will dynamically parse your prompt, delegate to agents, and the agents can execute real Python code, search the web, and read/write files!
```bash
macli swarm "Search the web for the latest Python version, write a simple script to print it, and execute it to verify."
```

### 5. Run a static Workflow
Execute a multi-agent workflow defined strictly in `agents.yaml`. By default, it runs the `research_and_write` workflow.
```bash
macli run "Build a simple Hello World in Python" --workflow research_and_write
```

### 6. Interactive Chat Mode
Want to chat directly with a single agent to test its skills? You can enter an interactive chat mode!
```bash
macli chat Researcher
```
Type `exit` or `quit` to leave the chat.

### 7. Auto-Saved Conversation Logs
Every time you run a workflow or chat with an agent, the full conversation is automatically exported as a Markdown file in the `outputs/` directory.

---

## 🧠 How to Add New Skills
The CLI provides a built-in generator to help you create new skills easily:
```bash
macli create-skill
```
This will launch a wizard asking for the skill name and description, and will automatically generate a `.md` file in the `skills/` directory with the proper YAML frontmatter.

For example, a `python-expert.md` skill looks like this:
```markdown
---
name: python-expert
description: You are a Python 3.10+ expert.
---

# Guidelines
1. Always use type hints.
2. Write clean, PEP8 compliant code.
```
Then, assign `python-expert` to any agent in `agents.yaml`.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! This is an educational project aimed at helping beginners understand AI agents without being overwhelmed by massive frameworks.

## 📝 License
This project is [MIT](LICENSE) licensed.
