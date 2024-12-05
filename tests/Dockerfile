# Use the Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies and Python libraries
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir requests unittest-xml-reporting

# Copy the application code into the container
# COPY test_gateway.py /app/test_gateway.py
COPY test_gateway.py /app/tests/test_gateway.py
# Specify the command to run the tests
ENTRYPOINT ["python3", "-m", "unittest", "discover", "-s", "/app/tests", "-p", "test_*.py"]
