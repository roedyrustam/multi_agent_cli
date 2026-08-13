import json
from rich.console import Console
from agent import Agent
from orchestrator import Orchestrator

console = Console()

class SwarmDirector:
    def __init__(self, config: dict):
        self.config = config
        self.orchestrator = Orchestrator(config)
        
        director_cfg = {
            "name": "Swarm Director",
            "role": "Master AI Orchestrator",
            "model": "gemini/gemini-2.5-flash",
            "description": "You manage a swarm of specialized AI agents. You analyze complex tasks and break them down into steps for your swarm. You must return ONLY valid JSON."
        }
        self.director_agent = Agent(director_cfg)

    def run_swarm(self, task: str):
        from logger import ConversationLogger
        logger = ConversationLogger("swarm", "director")
        logger.log_user(task)
        
        console.print("[bold magenta]Swarm Director is analyzing your task...[/bold magenta]")
        
        agents_info = []
        for ag in self.config.get("agents", []):
            agents_info.append(f"- Name: {ag.get('name')}, Role: {ag.get('role')}, Description: {ag.get('description')}")
            
        agents_list_str = "\n".join(agents_info)
        
        prompt = f"""
You are the Swarm Director. Break down this task into a sequential workflow using the available agents.
Task: {task}

Available Agents:
{agents_list_str}

Return a JSON array of objects, where each object has 'agent' (the exact name of the agent) and 'instructions' (the specific task for that agent).
DO NOT return markdown code blocks, just raw JSON.
        """
        
        with console.status("[bold yellow]Director is formulating a plan...[/bold yellow]", spinner="dots"):
            response = self.director_agent.chat(prompt)
            
        logger.log_agent("Swarm Director", response)
        
        try:
            clean_json = response.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:-3]
            elif clean_json.startswith("```"):
                clean_json = clean_json[3:-3]
                
            plan = json.loads(clean_json)
            
            console.print("[bold green]Swarm Director Plan Created![/bold green]")
            for step in plan:
                console.print(f"- [cyan]{step['agent']}[/cyan]: {step['instructions']}")
                
        except Exception as e:
            console.print(f"[bold red]Failed to parse Director's plan as JSON. Output was:[/bold red]\n{response}")
            return
            
        current_input = task
        for i, step in enumerate(plan):
            agent_name = step.get("agent")
            instructions = step.get("instructions")
            
            if agent_name not in self.orchestrator.agents:
                try:
                    from config import get_agent_config
                    agent_cfg = get_agent_config(agent_name, self.config)
                    self.orchestrator.agents[agent_name] = Agent(agent_cfg)
                except ValueError:
                    console.print(f"[bold red]Agent '{agent_name}' not found in configuration. Skipping.[/bold red]")
                    continue
                    
            agent = self.orchestrator.agents[agent_name]
            console.rule(f"[bold green]Step {i+1}: Executing Agent {agent_name} ({agent.role})[/bold green]")
            
            combined_prompt = f"Your specific task from the Director: {instructions}\n\nContext/Previous Output:\n{current_input}"
            
            with console.status(f"[bold yellow]{agent_name} is thinking and acting...[/bold yellow]", spinner="dots"):
                reply = agent.chat(combined_prompt)
                
            logger.log_agent(agent_name, reply)
            console.print(f"\n[cyan]{agent_name} Output:[/cyan]\n{reply}\n")
            current_input = reply
            
        console.rule("[bold magenta]Swarm Execution Complete[/bold magenta]")
        console.print(f"[green]Log saved to: {logger.get_filepath()}[/green]")
