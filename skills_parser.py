import os
import frontmatter
from pathlib import Path

# Cache to avoid rescanning every time
_GLOBAL_SKILLS_CACHE = {}

def get_search_paths():
    """Return a list of paths to scan for skills."""
    paths = [
        Path("skills").resolve(), # Local project skills
    ]
    
    # User home directory
    home = Path.home()
    
    # Antigravity Builtin
    ag_builtin = home / ".gemini" / "antigravity" / "builtin" / "skills"
    if ag_builtin.exists():
        paths.append(ag_builtin)
        
    # Antigravity / Claude Plugins
    plugins_dir = home / ".gemini" / "config" / "plugins"
    if plugins_dir.exists():
        # Add all 'skills' folders found inside plugins
        for plugin_folder in plugins_dir.iterdir():
            if plugin_folder.is_dir():
                skill_folder = plugin_folder / "skills"
                if skill_folder.exists():
                    paths.append(skill_folder)
                    
    return paths

def get_all_skills(force_refresh=False):
    """
    Scans all global paths and returns a dictionary:
    { "skill_name": {"path": "absolute_path", "source": "Local/Antigravity/VibesPlug", "description": "..."} }
    """
    global _GLOBAL_SKILLS_CACHE
    if _GLOBAL_SKILLS_CACHE and not force_refresh:
        return _GLOBAL_SKILLS_CACHE
        
    skills_registry = {}
    paths_to_scan = get_search_paths()
    
    for search_path in paths_to_scan:
        source_name = "Local"
        # Determine source
        path_str = str(search_path).replace("\\", "/")
        if ".gemini/antigravity/builtin" in path_str:
            source_name = "Antigravity Built-in"
        elif ".gemini/config/plugins" in path_str:
            plugin_name = search_path.parent.name
            source_name = f"Plugin: {plugin_name}"

        # In VibesPlug, skills can be inside folders like skills/skill-name/SKILL.md 
        # or directly skills/skill-name.md
        # Use rglob to find all .md files.
        for md_file in search_path.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    post = frontmatter.load(f)
                    
                metadata = post.metadata
                # Must have a 'name' in YAML frontmatter to be considered a skill
                if "name" in metadata:
                    skill_name = metadata["name"]
                    # If duplicate found, prioritize Local over Plugins
                    if skill_name not in skills_registry or source_name == "Local":
                        skills_registry[skill_name] = {
                            "path": str(md_file),
                            "source": source_name,
                            "description": metadata.get("description", "No description")
                        }
            except Exception:
                pass # Ignore files that are not valid YAML frontmatter or cannot be read

    _GLOBAL_SKILLS_CACHE = skills_registry
    return skills_registry

def load_skill(skill_name: str) -> str:
    """
    Loads a markdown skill file from the global registry,
    parses its YAML frontmatter, and returns the markdown content.
    """
    registry = get_all_skills()
    
    if skill_name not in registry:
        return f"Warning: Skill '{skill_name}' not found globally. Proceeding without it."
        
    skill_path = registry[skill_name]["path"]
    
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
            
        metadata = post.metadata
        content = post.content
        
        # Format the skill for the system prompt
        formatted_skill = f"\n--- SKILL: {metadata.get('name', skill_name)} ---\n"
        formatted_skill += f"Source: {registry[skill_name]['source']}\n"
        if 'description' in metadata:
            formatted_skill += f"Description: {metadata['description']}\n\n"
        formatted_skill += f"{content}\n--- END SKILL ---\n"
        
        return formatted_skill
    except Exception as e:
        return f"Error loading skill '{skill_name}': {str(e)}"
