#!/bin/bash
sudo bluetoothctl << EOF
power on
connect 85:55:A2:70:33:B3
exit
EOF