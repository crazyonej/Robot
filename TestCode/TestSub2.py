#!/usr/bin/env python3

from sh import bluetoothctl
mac = "85:55:A2:70:33:B3" 
bluetoothctl("connect ",mac)