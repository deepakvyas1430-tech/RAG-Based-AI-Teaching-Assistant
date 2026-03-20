import subprocess
import os
import sys
import time
import webbrowser
import signal

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "sigma-assistant")
NODE_PATH = r"C:\Program Files\nodejs"

# Update PATH to include Node.js
env = os.environ.copy()
env["PATH"] = f"{NODE_PATH};{env['PATH']}"

def run_process(command, cwd, title):
    print(f"[{title}] Starting in {cwd}...")
    try:
        # distinct_id is not a valid Popen argument on Windows, using creationflags usually for new console
        # primarily we just want to run it.
        # shell=True helps with resolving commands like 'npm' on windows sometimes, 
        # but 'cmd /c' is often safer for batch files or shell commands.
        # For uvicorn we can run module. For npm we need shell=True or fully qualified path.
        
        return subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE 
        )
    except Exception as e:
        print(f"[{title}] Failed to start: {e}")
        return None

def main():
    print("=" * 40)
    print(" SIGMA AI ASSISTANT - STARTUP SCRIPT")
    print("=" * 40)
    print(f"Project Root: {PROJECT_ROOT}")

    # 1. Start Backend
    backend_cmd = [sys.executable, "-m", "uvicorn", "server:app", "--reload", "--port", "8000"]
    # We pass the command as a string for shell=True or list for shell=False. 
    # With CREATE_NEW_CONSOLE, it's often easier to pass a string if using shell=True or 
    # to open a new terminal window. 
    
    # Let's use a specific command string that keeps the window open or at least identifiable.
    # On Windows, strictly `sys.executable` might need quoting if paths have spaces.
    backend_cmd_str = f'"{sys.executable}" -m uvicorn server:app --reload --host 0.0.0.0 --port 8000'
    
    backend_process = run_process(backend_cmd_str, PROJECT_ROOT, "BE")

    time.sleep(3) # Wait for backend to warm up

    # 2. Start Frontend
    # npm needs to be run through cmd /c or shell=True
    frontend_process = run_process("npm run dev -- --port 5173", FRONTEND_DIR, "FE")

    if not backend_process or not frontend_process:
        print("\n!!! Error starting one or more processes. Exiting. !!!")
        if backend_process: backend_process.terminate()
        if frontend_process: frontend_process.terminate()
        return

    # 3. Open Browser
    print("[Browser] Opening http://localhost:5173 ...")
    time.sleep(2)
    webbrowser.open("http://localhost:5173")

    print("\n" + "=" * 40)
    print(" APP RUNNING. Press Ctrl+C in this terminal to stop.")
    print("=" * 40)

    try:
        while True:
            time.sleep(1)
            # Check if processes are still alive
            if backend_process.poll() is not None:
                print("[BE] Backend process ended unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("[FE] Frontend process ended unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        if backend_process:
            backend_process.terminate()
            print("[BE] Stopped.")
        if frontend_process:
            frontend_process.terminate()
            print("[FE] Stopped.")
        print("Goodbye!")

if __name__ == "__main__":
    main()
