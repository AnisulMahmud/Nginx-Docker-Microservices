

FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install procps and Docker CLI
RUN apt-get update && apt-get install -y \
    procps \
    curl && \
    curl -fsSL https://get.docker.com | sh && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY app.py /app/app.py

# Install Python dependencies
RUN pip install --no-cache-dir flask

# Expose the application port
EXPOSE 5000

# Specify the entry point to run the application
ENTRYPOINT ["python", "app.py"]
