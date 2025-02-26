import subprocess
import os
import time

# Change the working directory to `src`
os.chdir("src")

# Running all Python files
subprocess.Popen(["python", "Prepbk.py"])
subprocess.Popen(["python", "Quiz.py"])
subprocess.Popen(["python", "Voic.py"])

# Keep process running
while True:
    time.sleep(1)
