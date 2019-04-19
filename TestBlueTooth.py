import bluetooth
#mac = "85:55:A2:70:33:B3"
#sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect("85:55:A2:70:33:B3")