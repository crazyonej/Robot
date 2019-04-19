
#!/usr/bin/env python3
import time
import subprocess

output = subprocess.Popen("sudo bluetoothctl", shell=True)
time.sleep(0.1)
output = subprocess.Popen("connect 85:55:A2:70:33:B3", shell=True)
#time.sleep(0.1)
#output = subprocess.check_output("quit", shell=True)
#time.sleep(2)