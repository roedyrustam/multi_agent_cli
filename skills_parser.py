import os
import frontmatter

def load_skill(skill_name: str, skills_dir: str = "skills") -> str:
    """
    Loads a markdown skill file from the skills directory,
    parses its YAML frontmatter, and returns the markdown content
    along with its metadata as a formatted string.
    """
    skill_path = os.path.join(skills_dir, f"{skill_name}.md")
    
    if not os.path.exists(skill_path):
        return f"Warning: Skill '{skill_name}' not found at {skill_path}. Proceeding without it."
    
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
            
        metadata = post.metadata
        content = post.content
        
        # Format the skill for the system prompt
        formatted_skill = f"\n--- SKILL: {metadata.get('name', skill_name)} ---\n"
        if 'description' in metadata:
            formatted_skill += f"Description: {metadata['description']}\n\n"
        formatted_skill += f"{content}\n--- END SKILL ---\n"
        
        return formatted_skill
    except Exception as e:
        return f"Error loading skill '{skill_name}': {str(e)}"

def get_all_skills(skills_dir: str = "skills"):
    """Returns a list of available skills in the skills directory."""
    if not os.path.exists(skills_dir):
        return []
    
    skills = []
    for filename in os.listdir(skills_dir):
        if filename.endswith(".md"):
            skills.append(filename[:-3])
    return skills
