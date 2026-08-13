import litellm
import json
from litellm import completion_cost
from skills_parser import load_skill
from tools.core_tools import CORE_TOOLS_SCHEMA, AVAILABLE_TOOLS_MAP

class Agent:
    def __init__(self, config: dict, skills_dir: str = "skills"):
        self.name = config.get("name", "Unnamed Agent")
        self.role = config.get("role", "AI Assistant")
        self.description = config.get("description", "")
        import os
        raw_model = config.get("model", "default")
        if raw_model == "default":
            self.model = os.getenv("DEFAULT_MODEL", "gemini/gemini-2.5-flash")
        else:
            self.model = raw_model
        
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
                skill_content = load_skill(skill_name)
                prompt += skill_content
                
        return prompt

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            max_loops = 5
            for _ in range(max_loops):
                response = litellm.completion(
                    model=self.model,
                    messages=self.messages,
                    tools=CORE_TOOLS_SCHEMA
                )
                
                # Track tokens and cost
                usage = getattr(response, 'usage', None)
                if usage:
                    self.total_tokens += getattr(usage, 'total_tokens', 0)
                
                try:
                    self.total_cost += completion_cost(completion_response=response)
                except Exception:
                    pass
                
                message = response.choices[0].message
                
                # Check for tool calls
                if not getattr(message, 'tool_calls', None):
                    reply = message.content or ""
                    self.messages.append({"role": "assistant", "content": reply})
                    return reply
                
                # Handle tool calls
                self.messages.append(message)
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        args = json.loads(tool_call.function.arguments)
                        if func_name in AVAILABLE_TOOLS_MAP:
                            func = AVAILABLE_TOOLS_MAP[func_name]
                            result = str(func(**args))
                        else:
                            result = f"Error: Tool '{func_name}' not found."
                    except Exception as e:
                        result = f"Error parsing/executing tool: {str(e)}"
                        
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": result
                    })

            return "Agent stopped after reaching maximum tool call loops."
            
        except Exception as e:
            return f"Error during completion: {str(e)}"
