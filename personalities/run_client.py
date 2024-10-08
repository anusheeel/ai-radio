import asyncio
import subprocess

async def run_client(script_name):
    # Use subprocess to run the client
    # Use subprocess to run the client
    print(f"Running client: {script_name}")
    process = await asyncio.create_subprocess_exec(
        'python3', script_name,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Print the output and errors from the client
    while True:
        output = await process.stdout.readline()
        if output == b'':
            # Check if the process has finished
            await process.wait()
            break
        if output:
            print(f'{script_name}: {output.decode().strip()}')

        err = await process.stderr.readline()
        if err:
            print(f'{script_name} (ERROR): {err.decode().strip()}')

async def main():
    # Run both clients concurrently
    await asyncio.gather(
        run_client('personalities/gpt_client.py'),
        run_client('personalities/claude_client.py')
    )

if __name__ == '__main__':
    print("Anusheel")
    asyncio.run(main())
