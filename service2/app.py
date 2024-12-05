
from flask import Flask, jsonify, request
import socket
import subprocess
from datetime import datetime
import os

app = Flask(__name__)
valid_username = "anisul-mahmud"
valid_password = "docker"

# Global variables
state = "INIT"
state_log = []

@app.route('/', methods=['GET'])
def service2_info():
    if state != "RUNNING":
        return jsonify({"message": f"Service2 is not in RUNNING state", "state": state}), 403

    # Gather system information
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

@app.route('/state', methods=['GET', 'PUT'])
def manage_state():
    global state
    if request.method == 'GET':
        return state, 200

    # Handle state change requests
    new_state = request.data.decode('utf-8').strip().upper()
    if new_state not in ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"]:
        return "Invalid state", 400

    if new_state == state:
        return "No change in state", 200

    if new_state == "INIT":
        state_log.append(f"{datetime.utcnow().isoformat()}: {state}->INIT")
        state = "INIT"
        # Add any additional reset logic heress
        return jsonify({"message": "State changed to INIT. System reset.", "login_required": True}), 200

    if new_state == "RUNNING":
        if request.headers.get('Authorization') is None:
            return "Login required to transition to RUNNING", 403
        state_log.append(f"{datetime.utcnow().isoformat()}: {state}->RUNNING")
        state = "RUNNING"
        return "State changed to RUNNING", 200

    if new_state == "PAUSED":
        state_log.append(f"{datetime.utcnow().isoformat()}: {state}->PAUSED")
        state = "PAUSED"
        return "State changed to PAUSED", 200

    if new_state == "SHUTDOWN":
        state_log.append(f"{datetime.utcnow().isoformat()}: {state}->SHUTDOWN")
        state = "SHUTDOWN"
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
                try:
                    # Stop all containers
                    stop_result = subprocess.run(
                        ["docker", "stop"] + container_ids,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    stopped_containers = stop_result.stdout.decode('utf-8').strip().split('\n')
                    if not stopped_containers or stopped_containers[0] == '':
                        # All containers have been stopped
                        return jsonify({"message": "System has been shut down successfully. All containers have been stopped."}), 200
                    else:
                        return jsonify({"message": f"State changed to SHUTDOWN. Stopped containers: {', '.join(stopped_containers)}"}), 200
                except subprocess.CalledProcessError as stop_error:
                    stop_error_message = stop_error.stderr.decode('utf-8')
                    print(f"Error stopping containers: {stop_error_message}")
                    return jsonify({"error": f"Failed to stop containers: {stop_error_message}"}), 500
            else:
                # No running containers
                return jsonify({"message": "State changed to SHUTDOWN. No running containers to stop."}), 200
        except subprocess.CalledProcessError as e:
            ps_error_message = e.stderr.decode('utf-8')
            print(f"Error getting container IDs: {ps_error_message}")
            return jsonify({"error": f"Failed to retrieve container IDs: {ps_error_message}"}), 500
        except Exception as e:
            print(f"Unexpected error during SHUTDOWN: {str(e)}")
            return jsonify({"error": f"Unexpected error during SHUTDOWN: {str(e)}"}), 500
        




@app.route('/run-log', methods=['GET'])
def run_log():
    return "\n".join(state_log), 200

@app.route('/request', methods=['GET'])
def handle_request():
    if state != "RUNNING":
        return jsonify({"message": f"Service2 is not in RUNNING state", "state": state}), 403

    # Return system info when in RUNNING state
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
