import subprocess
import os

while 'dist' in os.getcwd():
    os.chdir('..')

# executes main.py in the terminal
cmd = subprocess.Popen(["start", "cmd", "/k", f"python {os.getcwd()}\main.py"], shell=True)
