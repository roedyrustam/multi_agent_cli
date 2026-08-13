import os
import yaml
from dotenv import load_dotenv

def load_config(config_path: str = "agents.yaml"):
    """Loads environment variables and the YAML configuration."""
    load_dotenv()  # Load .env variables

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config

def get_agent_config(agent_name: str, config: dict):
    """Retrieves configuration for a specific agent."""
    agents = config.get("agents", [])
    for agent in agents:
        if agent.get("name") == agent_name:
            return agent
    raise ValueError(f"Agent '{agent_name}' not found in configuration.")

def get_workflow_config(workflow_name: str, config: dict):
    """Retrieves configuration for a specific workflow."""
    workflows = config.get("workflows", [])
    for workflow in workflows:
        if workflow.get("name") == workflow_name:
            return workflow
    raise ValueError(f"Workflow '{workflow_name}' not found in configuration.")
