
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
            # Stop all containerss
            result = subprocess.run(["docker-compose", "down"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return f"State changed to SHUTDOWN. Services stopped: {result.stdout.decode('utf-8')}", 200
        except subprocess.CalledProcessError as e:
            return f"Error during SHUTDOWN: {e.stderr.decode('utf-8')}", 500

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
