FROM python:3.9-slim


# Set the working directory
WORKDIR /app


# Install procps to get the ps command
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents intot the container 
COPY app.py /app/app.py

# Install any needed packages
RUN pip install --no-cache-dir flask


# Expose the port of my application runs on
EXPOSE 5000

# Specify the entry point to run the compiled java class
ENTRYPOINT [ "python", "app.py" ]
