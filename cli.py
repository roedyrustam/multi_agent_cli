import os
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from config import load_config
from orchestrator import Orchestrator
from skills_parser import get_all_skills

app = typer.Typer(help="Multi-Agent CLI for Vibes-Plug Ecosystem")
console = Console()

@app.command()
def setup():
    """Interactive setup wizard for API Keys."""
    console.print("[bold yellow]Welcome to the Setup Wizard![/bold yellow]")
    console.print("Let's configure your API keys. You can leave a key blank if you don't plan to use that provider.\n")
    
    gemini_key = Prompt.ask("Enter your GEMINI_API_KEY (from Google AI Studio)", default="")
    groq_key = Prompt.ask("Enter your GROQ_API_KEY (from Groq Console)", default="")
    openai_key = Prompt.ask("Enter your OPENAI_API_KEY", default="")
    
    env_content = f"GEMINI_API_KEY={gemini_key}\nGROQ_API_KEY={groq_key}\nOPENAI_API_KEY={openai_key}\n"
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
        
    console.print("\n[bold green]Success![/bold green] Your keys have been saved to .env")

@app.command()
def run(task: str, workflow: str = typer.Option("research_and_write", "--workflow", "-w", help="Name of the workflow to run")):
    """Runs a specific workflow with the given task."""
    if not os.path.exists(".env"):
        console.print("[yellow]No .env file found. Running initial setup...[/yellow]\n")
        setup()
        
    try:
        config = load_config()
        orch = Orchestrator(config)
        orch.run_workflow(workflow, task)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@app.command()
def list_skills():
    """Lists all available skills in the skills directory."""
    skills = get_all_skills()
    if not skills:
        console.print("[yellow]No skills found in the skills/ directory.[/yellow]")
        return
        
    table = Table(title="Available Skills")
    table.add_column("Skill Name", style="cyan")
    
    for skill in skills:
        table.add_row(skill)
        
    console.print(table)

@app.command()
def list_agents():
    """Lists all configured agents."""
    try:
        config = load_config()
        agents = config.get("agents", [])
        
        table = Table(title="Configured Agents")
        table.add_column("Name", style="cyan")
        table.add_column("Role", style="magenta")
        table.add_column("Model", style="green")
        table.add_column("Skills", style="yellow")
        
        for agent in agents:
            skills_str = ", ".join(agent.get("skills", []))
            table.add_row(agent.get("name"), agent.get("role"), agent.get("model"), skills_str)
            
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    console.print("[bold magenta]Welcome to Multi-Agent CLI![/bold magenta]")
    app()
