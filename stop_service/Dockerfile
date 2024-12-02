# # Use an appropriate base image
# FROM python:3.9-slim

# RUN apt-get update && \
#     apt-get install -y \
#     curl \
#     ca-certificates \
#     gnupg \
#     lsb-release \
#     && curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose \
#     && chmod +x /usr/local/bin/docker-compose \
#     && apt-get clean

# # Install Docker (needed for docker-compose commands)
# RUN curl -fsSL https://get.docker.com | bash

# # Set the working directory
# WORKDIR /app

# # Install any Python dependencies (if needed)
# COPY requirements.txt /app/
# RUN pip install -r requirements.txt

# # Copy your application files
# COPY . /app/

# # Command to run your Flask app
# CMD ["python", "stop_service/stop_service.py"]
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && apt-get install -y docker.io \
    && apt-get clean

# Install Python dependencies
RUN pip install flask

# Set the working directory
WORKDIR /app

# Copy the stop service code
# COPY ./stop_service /app/stop_service

# Expose the necessary port
EXPOSE 8210

CMD ["python", "/app/stop_service/stop_service.py"]
