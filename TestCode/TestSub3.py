#!/usr/bin/env python3
import pexpect
from sh import bluetoothctl
import subprocess
mac = "85:55:A2:70:33:B3"
#sh.bluetoothctl("pair", mac)
print ("stuck here")
#bluetoothctl("connect", mac)
child = pexpect.spawn('bluetoothctl')
child.sendline('power on')
child.sendline('agent on')
child.sendline('default-agent')
child.sendline('pair 85:55:A2:70:33:B3')
child.sendline('trust 85:55:A2:70:33:B3')
child.sendline('connect 85:55:A2:70:33:B3')
