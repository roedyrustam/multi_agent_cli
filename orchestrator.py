from agent import Agent
from config import get_workflow_config, get_agent_config
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class Orchestrator:
    def __init__(self, config: dict):
        self.config = config
        self.agents = {}
        
    def initialize_agents(self, workflow_name: str):
        workflow = get_workflow_config(workflow_name, self.config)
        
        steps = workflow.get("steps", [])
        for step in steps:
            agent_name = step.get("agent")
            if agent_name not in self.agents:
                agent_cfg = get_agent_config(agent_name, self.config)
                self.agents[agent_name] = Agent(agent_cfg)
                
        return workflow

    def run_workflow(self, workflow_name: str, task: str):
        workflow = self.initialize_agents(workflow_name)
        
        current_input = task
        console.print(f"[bold blue]Starting workflow:[/bold blue] {workflow_name}")
        console.print(f"[bold blue]Initial Task:[/bold blue] {task}\n")
        
        steps = workflow.get("steps", [])
        for i, step in enumerate(steps):
            agent_name = step.get("agent")
            agent = self.agents[agent_name]
            
            console.rule(f"[bold green]Step {i+1}: Executing Agent {agent_name} ({agent.role})[/bold green]")
            
            if i == 0:
                prompt = current_input
            else:
                prompt = f"Original Task: {task}\n\nPrevious Agent Output to review/build upon:\n{current_input}"
                
            with console.status(f"[bold yellow]{agent_name} is thinking...[/bold yellow]", spinner="dots"):
                reply = agent.chat(prompt)
            
            console.print(Panel(Markdown(reply), title=f"{agent_name} Output", border_style="green"))
            current_input = reply
            
        console.rule(f"[bold blue]Workflow '{workflow_name}' Completed[/bold blue]")
        return current_input
