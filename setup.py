from setuptools import setup, find_packages

setup(
    name="multi-agent-cli",
    version="1.0.0",
    py_modules=["cli", "agent", "orchestrator", "logger", "config", "skills_parser", "director"],
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "litellm>=1.0.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "duckduckgo-search>=5.3.0"
    ],
    entry_points={
        "console_scripts": [
            "macli=cli:app",
            "swarmcli=cli:app"
        ],
    },
)
