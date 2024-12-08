
from flask import Flask, jsonify, request
from threading import Lock
import socket
import subprocess
from datetime import datetime, timezone
import os
from threading import Thread
from functools import wraps

app = Flask(__name__)

# Global variables
state = "INIT"
state_log = []
start_time = datetime.now(timezone.utc)  # Track service start time


request_count_lock = Lock()
request_count = 0

# Decorator to ensure thread-safe request counting
def count_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global request_count
        with request_count_lock:
            request_count += 1
            print(f"Request count incremented to {request_count}")
        return func(*args, **kwargs)
    return wrapper



# Service endpoints and functions

# Service information endpoint -> Endpoint to provide Service2 information when the state is RUNNING.

@app.route('/', methods=['GET'])
def service2_info():
    """Provide service information if the state is RUNNING."""
    # Check if the service is in RUNNING state
    if state != "RUNNING":
        return jsonify({"message": "Service2 is not in RUNNING state", "state": state}), 403
    
    try:
        info = {
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "Processes": subprocess.check_output(['ps', '-eo', 'pid,user,time,comm']).decode('utf-8').strip().split('\n'),
            "FreeSpaceGB": f"{os.statvfs('/').f_frsize * os.statvfs('/').f_bavail / (1024 * 1024 * 1024):.2f}",
            "Last Boot Time": datetime.strptime(
                subprocess.check_output(['uptime', '-s']).decode('utf-8').strip(),
                '%Y-%m-%d %H:%M:%S'
            ).strftime('%a %b %d %H:%M:%S GMT %Y'),
            "State": state
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# State management endpoints -> manage the system state and provide the run log
@app.route('/state', methods=['GET', 'PUT'])
def manage_state():
    """Get or update the system state."""
    global state
    if request.method == 'GET':
        # Return the current state without forcing re-authentication
        return jsonify({"state": state}), 200

    # Handle state change requests
    new_state = request.data.decode('utf-8').strip().upper()
    if new_state not in ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"]:
        return jsonify({"error": "Invalid state"}), 400

    if new_state == state:
        return jsonify({"message": "No change in state"}), 200
    
    # Handle INIT state
    if new_state == "INIT":
        state_log.append(f"{datetime.now(timezone.utc).isoformat()}: {state}->INIT")
        state = "INIT"
        # Return a 401 Unauthorized response to force the user to re-authenticate
        response = jsonify({"message": "State changed to INIT. Please re-authenticate."})
        response.headers['WWW-Authenticate'] = 'Basic realm="Restricted Access"'
        response.status_code = 401
        return response
    
    # Handle RUNNING state
    if new_state == "RUNNING":
        if request.headers.get('Authorization') is None:
            return jsonify({"error": "Login required to transition to RUNNING"}), 403
        state_log.append(f"{datetime.now(timezone.utc).isoformat()}: {state}->RUNNING")
        state = "RUNNING"
        return jsonify({"message": "State changed to RUNNING"}), 200

    # Handle PAUSED state
    if new_state == "PAUSED":
        state_log.append(f"{datetime.now(timezone.utc).isoformat()}: {state}->PAUSED")
        state = "PAUSED"
        return jsonify({"message": "State changed to PAUSED"}), 200
    
    # Handle SHUTDOWN state
    if new_state == "SHUTDOWN":
        state_log.append(f"{datetime.now(timezone.utc).isoformat()}: {state}->SHUTDOWN")
        state = "SHUTDOWN"

        # Start container shutdown 
        Thread(target=shutdown_containers).start()

        return jsonify({"message": "State changed to SHUTDOWN. Stopping all containers..."}), 200


def shutdown_containers():
    """Shutdown all running Docker containers."""
    try:
        # Get IDs of all running containers
        result = subprocess.run(
            ["docker", "ps", "-q"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        container_ids = result.stdout.decode('utf-8').strip().split('\n')

        if container_ids and container_ids[0]:  # Check if there are running containers
            stop_result = subprocess.run(
                ["docker", "stop"] + container_ids,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stopped_containers = stop_result.stdout.decode('utf-8').strip().split('\n')
            print(f"Stopped containers: {stopped_containers}")
        else:
            print("No running containers to stop.")
    except subprocess.CalledProcessError as e:
        print(f"Error during container shutdown: {e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"Unexpected error during SHUTDOWN: {str(e)}")


@app.route('/run-log', methods=['GET'])
def run_log():
    """Fetch the run log."""
    return "\n".join(state_log), 200



@app.route('/check-state', methods=['GET'])
def check_state():
    """Provide a simple endpoint to check the current state."""
    return jsonify({"state": state}), 200

# Request endpoint -> handle system requests and provide useful system info

@app.route('/request', methods=['GET'])
@count_request
def handle_request():
    """Handle system request if in RUNNING state."""
    print(f"Handle request endpoint called: {request.url}")


    if request.path == '/favicon.ico':
        print("Ignoring favicon.ico request")
        return "", 204
    
    # Check if the service is in RUNNING state
    if state != "RUNNING":
        return jsonify({"message": "Service2 is not in RUNNING state", "state": state}), 403
    print(f"/request endpoint called while state is RUNNING.")
    try:
        info = {
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "Processes": subprocess.check_output(['ps', '-eo', 'pid,user,time,comm']).decode('utf-8').strip().split('\n'),
            "FreeSpaceGB": f"{os.statvfs('/').f_frsize * os.statvfs('/').f_bavail / (1024 * 1024 * 1024):.2f}",
            "Last Boot Time": datetime.strptime(
                subprocess.check_output(['uptime', '-s']).decode('utf-8').strip(),
                '%Y-%m-%d %H:%M:%S'
            ).strftime('%a %b %d %H:%M:%S GMT %Y'),
            "State": state
        }
        return jsonify(info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Metrics endpoint -> retrieve useful info about the service uptime, request count, and state  
@app.route('/metrics', methods=['GET'])
def get_metrics():
    print("Metrics endpoint called")  
    uptime = datetime.now(timezone.utc)- start_time
    metrics = {
        "Service Start Time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "Uptime (seconds)": str(uptime.total_seconds()),
        "Request Count": request_count,
        "State": state
    }
    print(f"Metrics: {metrics}")  # Log the metrics
    return jsonify(metrics)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
