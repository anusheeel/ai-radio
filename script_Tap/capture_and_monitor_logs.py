from script_Tap.run_uvicorn import run_uvicorn, run_client_script
def monitor_processes(uvicorn_process, client_process):
    try:
        while True:
            # Read `uvicorn` output
            uvicorn_output = uvicorn_process.stdout.readline()
            if uvicorn_output:
                print(f"Uvicorn: {uvicorn_output.strip()}")

            uvicorn_error_output = uvicorn_process.stderr.readline()
            if uvicorn_error_output:
                print(f"Uvicorn ERROR: {uvicorn_error_output.strip()}")

            # Read client output
            client_output = client_process.stdout.readline()
            if client_output:
                print(f"Client: {client_output.strip()}")

            client_error_output = client_process.stderr.readline()
            if client_error_output:
                print(f"Client ERROR: {client_error_output.strip()}")

            # Stop if both processes are done
            if (
                uvicorn_output == "" and uvicorn_error_output == "" and uvicorn_process.poll() is not None
                and client_output == "" and client_error_output == "" and client_process.poll() is not None
            ):
                break

    except KeyboardInterrupt:
        print("Shutting down processes...")
        uvicorn_process.terminate()
        client_process.terminate()
        uvicorn_process.wait()
        client_process.wait()

    print("Processes finished.")

if __name__ == "__main__":
    # Step 1: Start `uvicorn`
    uvicorn_process = run_uvicorn()

    # Step 2: Start the client script after `uvicorn` is running
    client_process = run_client_script()

    # Step 3: Monitor both processes
    monitor_processes(uvicorn_process, client_process)
