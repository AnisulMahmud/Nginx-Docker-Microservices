from flask import Flask, jsonify
import subprocess
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Method to run a Bash script
def run_bash_script(script_path):
    try:
        logging.debug(f"Running bash script at {script_path}")
        
        # Run the Bash script
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
        
        # Log the output
        logging.debug(f"Script output: {result.stdout}")
        logging.debug(f"Script error: {result.stderr}")
        
        if result.returncode == 0:
            return True
        else:
            logging.error(f"Script failed with error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing the bash script: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

# Method to run Docker Compose command directly
def run_docker_compose_command(command):
    try:
        logging.debug(f"Running Docker Compose command: {command}")
        
        # Run the docker-compose command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            cwd=os.getcwd()  # Ensure we're in the correct directory where docker-compose.yml is located
        )
        
        # Log the output
        logging.debug(f"Docker Compose output: {result.stdout}")
        logging.debug(f"Docker Compose error: {result.stderr}")
        
        if result.returncode == 0:
            return True
        else:
            logging.error(f"Docker Compose failed with error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing Docker Compose command: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return False

@app.route("/api/stop", methods=["POST"])
def stop_all_services():
    script_path = "/app/stop_service/stop_containers.sh"  # Path to your Bash script
    
    # Try running the Bash script first
    if run_bash_script(script_path):
        return jsonify(message="All services stopped successfully using Bash script."), 200
    
    # If the Bash script fails, run Docker Compose down as a fallback
    logging.error("Bash script failed, attempting to run Docker Compose command...")
    
    command = ["docker-compose", "down"]  # The Docker Compose command to stop all services
    
    if run_docker_compose_command(command):
        return jsonify(message="All services stopped successfully using Docker Compose."), 200
    else:
        return jsonify(message="Failed to stop services with both methods."), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8210)
