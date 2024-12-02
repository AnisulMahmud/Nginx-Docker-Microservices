#!/bin/bash

# Navigate to the directory where the docker-compose.yml file is located
cd /app  # Replace with your actual project directory

# Stop and remove all containers, networks, and volumes defined in docker-compose.yml
docker-compose down --volumes --rmi all --remove-orphans

# Optionally clean up unused Docker resources (e.g., volumes, networks, etc.)
docker system prune -f
