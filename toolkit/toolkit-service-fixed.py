from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import subprocess
import psutil
import os
import signal
import time
import threading

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
CORS(app)

class Scan:
    def __init__(self):
        self.scan_running = False
        self.scan_step = 0
        self.scan_complete = 0
        self.scan_step_name = "N/a"
        self.scan_target = "N/a"
        self.core_module = "N/a"
        self.active_processes = []
        self.process_lock = threading.Lock()

scan_obj = Scan()

def start_scan(fire_starter, fire_cloud, fire_scanner, domain_count, core_module):
    global scan_obj
    scan_obj.scan_running = True
    scan_obj.scan_step = 1
    counter = 0
    if fire_starter:
        counter += 14
    if fire_cloud:
        counter += 8
    if fire_scanner:
        counter += 12
    scan_obj.scan_complete = counter * domain_count
    scan_obj.core_module = core_module
    scan_obj.scan_step_name = "Starting..."
    scan_obj.scan_target = "Sorting..."

def stop_scan():
    global scan_obj
    # First, ensure all processes are terminated
    cancel_subprocesses()
    # Then reset the scan state
    scan_obj.scan_running = False
    scan_obj.scan_step = 0
    scan_obj.scan_complete = 0
    scan_obj.scan_step_name = "Not Running"
    scan_obj.core_module = "N/a"
    scan_obj.scan_target = "N/a"
    with scan_obj.process_lock:
        scan_obj.active_processes = []

def kill_process_tree(pid):
    """Kill a process and all its children"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # First, try to terminate children gracefully
        for child in children:
            try:
                child.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Give processes some time to terminate
        _, still_alive = psutil.wait_procs(children, timeout=3)
        
        # If any process is still alive, kill it forcefully
        for child in still_alive:
            try:
                child.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            
        # Finally terminate the parent if it's not the current process
        if pid != os.getpid():
            parent.terminate()
            try:
                parent.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.TimeoutExpired):
                parent.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"Error terminating process {pid}: {str(e)}")

def cancel_subprocesses():
    """Improved function to terminate all child processes and their descendants"""
    current_pid = os.getpid()
    
    # Kill all tracked processes
    with scan_obj.process_lock:
        for proc in scan_obj.active_processes:
            if proc.is_alive():
                print(f"Terminating tracked process {proc.pid}")
                kill_process_tree(proc.pid)
        
        # Also search for any other child processes that might not be tracked
        all_processes = psutil.process_iter(attrs=['pid', 'ppid', 'cmdline'])
        for process in all_processes:
            pid = process.info['pid']
            ppid = process.info['ppid']
            if ppid == current_pid and pid != current_pid:
                print(f"Terminating untracked subprocess {pid}")
                kill_process_tree(pid)
        
        # Clear the tracked processes list
        scan_obj.active_processes = []

@app.route('/terminate-subprocesses', methods=['GET'])
def terminate_subprocesses():
    try:
        cancel_subprocesses()
        return jsonify({'message': 'Subprocesses terminated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message":"pong!"})

@app.route('/status', methods=['GET'])
def status():
    global scan_obj
    if scan_obj.scan_running:
        return jsonify({
            "scan_running":True,
            "scan_step":scan_obj.scan_step,
            "scan_complete":scan_obj.scan_complete,
            "scan_step_name":scan_obj.scan_step_name,
            "scan_target":scan_obj.scan_target,
            "core_module":scan_obj.core_module
            })
    else:
        return jsonify({
            "scan_running":False,
            "scan_step":scan_obj.scan_step,
            "scan_complete":scan_obj.scan_complete,
            "scan_step_name":scan_obj.scan_step_name,
            "scan_target":scan_obj.scan_target
            })
    
@app.route('/update-scan', methods=['POST'])
def update_scan():
    global scan_obj
    if scan_obj.scan_running:
        data = request.get_json()
        scan_obj.scan_step += 1
        scan_obj.scan_step_name = data['stepName']
        scan_obj.scan_target = data['target_domain']
        return jsonify({
                "scan_running":scan_obj.scan_running,
                "scan_step":scan_obj.scan_step,
                "scan_step_name":scan_obj.scan_step_name,
                "target_domain":scan_obj.scan_target
                })
    else:
        return jsonify({"message": "ERROR: Scan Not Currently Running..."})

def run_subprocess(command, shell=True):
    """Run a subprocess and track it for proper termination later"""
    process = subprocess.Popen(command, shell=shell)
    with scan_obj.process_lock:
        scan_obj.active_processes.append(psutil.Process(process.pid))
    return process

@app.route('/wildfire', methods=['POST'])
def wildfire():
    global scan_obj
    if not scan_obj.scan_running:
        data = request.get_json()
        fire_starter = data['fireStarter']
        fire_cloud = data['fireCloud']
        fire_scanner = data['fireScanner']
        fqdn = data.get('fqdn', '')
        scan_single_domain = data.get('scanSingleDomain', False)
        domain_count = data.get('domainCount', 1)
        start_flag, cloud_flag, scan_flag, fqdn_flag, scanSingle_flag  = "", "", "", "", ""
        if fire_starter:
            start_flag = " --start"
        if fire_cloud:
            cloud_flag = " --cloud"
        if fire_scanner:
            scan_flag = " --scan"
        if scan_single_domain:
            fqdn_flag = f" --fqdn {fqdn}"
            scanSingle_flag = f" --scanSingle"
        scan_obj.core_module = "Wildfire.py"
        start_scan(fire_starter, fire_cloud, fire_scanner, domain_count, scan_obj.core_module)
        
        # Use the tracking function instead of direct subprocess call
        process = run_subprocess(f"python3 wildfire.py{start_flag}{cloud_flag}{scan_flag}{fqdn_flag}{scanSingle_flag}")
        process.wait()  # Wait for completion
        
        stop_scan()
        return jsonify({"message": "Done!"})
    else:
        return jsonify({"message": "ERROR: Scan Running..."})

@app.route('/collect_sceenshots', methods=['POST'])
def collect_sceenshots():
    process = run_subprocess(f"python3 wildfire.py --screenshots")
    process.wait()  # Wait for completion
    return jsonify({"message": "Done!"})

if __name__ == '__main__':
    app.run(debug=True)
