# 🚀 VibesAgent-CLI

A lightweight, beginner-friendly Python Command Line Interface (CLI) for orchestrating multiple AI agents. Built with **LiteLLM**, **Typer**, and **Rich**, this tool makes it incredibly easy to experiment with multi-agent workflows using any LLM provider (OpenAI, Anthropic, Gemini, Groq, Ollama, etc.)—even on free tiers!

This project features native integration with the **Vibes-Plug** ecosystem, allowing agents to automatically learn new "skills" from simple Markdown files.

## ✨ Features
- **Multi-Provider Support**: Switch between Gemini, LLaMA (via Groq), Claude, or GPT models effortlessly using `LiteLLM`.
- **Markdown Skill Injection**: Define expert skills in Markdown (`skills/` directory) and they will be automatically injected into your agent's system prompt.
- **Beautiful Terminal UI**: Uses `Rich` for gorgeous tables, colors, and loading animations.
- **YAML Configuration**: Easily define your agents, their roles, and step-by-step workflows in `agents.yaml`.
- **Beginner Friendly**: No heavy abstractions like LangGraph or AutoGen—just pure, transparent Python code that is easy to study and modify.

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi-agent-cli.git
   cd multi-agent-cli
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Rename `.env.example` to `.env` and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_key
   GROQ_API_KEY=your_groq_key
   OPENAI_API_KEY=your_openai_key
   ```

---

## 🚀 Usage

### 1. Check Available Skills
List all skills currently loaded in your `skills/` directory:
```bash
python cli.py list-skills
```

### 2. Check Configured Agents
View the agents defined in your `agents.yaml`:
```bash
python cli.py list-agents
```

### 3. Run a Workflow
Execute a multi-agent workflow defined in `agents.yaml`. By default, it runs the `research_and_write` workflow.
```bash
python cli.py run "Build a simple Hello World in Python" --workflow research_and_write
```

---

## 🧠 How to Add New Skills
Simply drop a new Markdown file into the `skills/` directory. It must include YAML frontmatter at the top. For example, `skills/python-expert.md`:

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
