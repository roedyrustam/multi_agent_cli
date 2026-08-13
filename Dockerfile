FROM python:3.10-slim

WORKDIR /app

# Install git since some skills might require fetching code later (optional but good practice)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command can be overridden by docker-compose
CMD ["python", "cli.py", "run", "Hello AI", "--workflow", "research_and_write"]
