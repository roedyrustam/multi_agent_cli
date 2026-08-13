import os
from datetime import datetime

from config import get_base_dir

class ConversationLogger:
    def __init__(self, mode: str, name: str):
        self.mode = mode
        self.name = name
        outputs_dir = os.path.join(get_base_dir(), "outputs")
        os.makedirs(outputs_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(outputs_dir, f"{mode}_{name}_{timestamp}.md")
        
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(f"# Multi-Agent CLI Log\n")
            f.write(f"**Mode:** {mode}\n")
            f.write(f"**Target:** {name}\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"---\n\n")

    def log_user(self, text: str):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"### 👤 User\n{text}\n\n")
            
    def log_agent(self, agent_name: str, text: str):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"### 🤖 Agent: {agent_name}\n{text}\n\n")
            
    def get_filepath(self):
        return self.filepath
