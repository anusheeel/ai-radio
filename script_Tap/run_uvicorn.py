import subprocess
import time

def run_client_script():
    # Start the client script as a subprocess
    client_command = ["python3", "personalities/run_client.py"]

    client_process = subprocess.Popen(
        client_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    
