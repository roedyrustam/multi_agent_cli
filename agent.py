import litellm
from skills_parser import load_skill

class Agent:
    def __init__(self, config: dict, skills_dir: str = "skills"):
        self.name = config.get("name", "Unnamed Agent")
        self.role = config.get("role", "AI Assistant")
        self.description = config.get("description", "")
        self.model = config.get("model", "gemini/gemini-2.5-flash")
        
        # Load skills and build system prompt
        self.skills = config.get("skills", [])
        self.system_prompt = self._build_system_prompt(skills_dir)
        
        # Conversation history
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def _build_system_prompt(self, skills_dir: str) -> str:
        prompt = f"You are a {self.role}. {self.description}\n\n"
        
        if self.skills:
            prompt += "You have been equipped with the following specialized skills. Follow their instructions strictly:\n"
            for skill_name in self.skills:
                skill_content = load_skill(skill_name, skills_dir)
                prompt += skill_content
                
        return prompt

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            response = litellm.completion(
                model=self.model,
                messages=self.messages
            )
            
            reply = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reply})
            return reply
            
        except Exception as e:
            return f"Error during completion: {str(e)}"
