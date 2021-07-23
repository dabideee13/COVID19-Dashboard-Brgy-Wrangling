import subprocess
import os

# executes main.py in the terminal
cmd1 = subprocess.Popen(["start", "cmd", "/k",
                      "py C:/Users/Admin/Documents/GitHub/COVID19-Dashboard-Brgy-Wrangling/main.py"],
                      shell = True)

