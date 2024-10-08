import logging
import subprocess
from script_Tap.run_uvicorn import run_client_script

def run_uvicorn():
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("uvicorn.log"),
            logging.StreamHandler()
        ]
    )

    # Run uvicorn as a subprocess
    uvicorn_process = subprocess.Popen(
        ["uvicorn", "orchestrator.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return uvicorn_process

if __name__ == "__main__":
    # Start uvicorn
    uvicorn_process = run_uvicorn()
    
    # Start the client script
    run_client_script()
    
    # Optionally, capture uvicorn's output
    try:
        while True:
            output = uvicorn_process.stdout.readline()
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        # Handle cleanup on exit
        uvicorn_process.terminate()
