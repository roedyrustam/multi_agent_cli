import litellm
from litellm import completion_cost
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
        
        # Tracking
        self.total_tokens = 0
        self.total_cost = 0.0
        
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
            
            # Track tokens and cost
            usage = getattr(response, 'usage', None)
            if usage:
                self.total_tokens += getattr(usage, 'total_tokens', 0)
            
            try:
                self.total_cost += completion_cost(completion_response=response)
            except Exception:
                pass
            
            reply = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reply})
            return reply
            
        except Exception as e:
            return f"Error during completion: {str(e)}"
