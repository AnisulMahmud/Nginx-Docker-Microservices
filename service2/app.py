from flask import Flask, jsonify
import socket
import subprocess
from datetime import datetime

import os

app = Flask(__name__)

@app.route('/')
def service2_info():
   
    info = {}

 

    # IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    info["IP Address"] = ip_address


    # Process list those are running 
    process = subprocess.check_output(['ps', '-eo', 'pid,user,time,comm'])
    process_list = process.decode('utf-8').strip().split('\n')
    info["Processes"] = process_list


    
    # Available disk
    statvfs = os.statvfs('/')
    free = statvfs.f_frsize * statvfs.f_bavail
    free_gb = free / (1024 * 1024 * 1024)  
    info["FreeSpaceGB"] = f"{free_gb:.2f}"


    # Last boot time
    boot_time = subprocess.check_output(['uptime', '-s'])
    last_boot_time = boot_time.decode('utf-8').strip()
    last_boot_time_formatted = datetime.strptime(last_boot_time, '%Y-%m-%d %H:%M:%S').strftime('%a %b %d %H:%M:%S GMT %Y')
    info["Last Boot Time"] = last_boot_time_formatted


    return jsonify(info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    

