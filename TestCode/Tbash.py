#!/usr/bin/env python3

import subprocess
import time #import time module

subprocess.Popen(["bash", "cam.sh"])
time.sleep(1.5)
subprocess.Popen(["bash", "strm.sh"])