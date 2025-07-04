import subprocess

# Start status_server.py in the background
subprocess.Popen(["python", "status_server.py"])

# Start main.py in the foreground (your bot or main app)
subprocess.run(["python", "main.py"])
