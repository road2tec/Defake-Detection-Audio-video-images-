import os
import subprocess
import re

def kill_port(port):
    print(f"Looking for process on port {port}...")
    try:
        # Run netstat
        output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        lines = output.strip().split('\n')
        
        pids = set()
        for line in lines:
            parts = line.split()
            # PID is the last column
            if parts:
                pid = parts[-1]
                pids.add(pid)
        
        if not pids:
            print(f"No process found on port {port}.")
            return

        for pid in pids:
            if pid == "0": continue
            print(f"Killing PID {pid}...")
            os.system(f"taskkill /F /PID {pid}")
            print(f"Killed PID {pid}")
            
    except subprocess.CalledProcessError:
        print(f"No process found on port {port} (netstat returned error).")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    kill_port(8000)
