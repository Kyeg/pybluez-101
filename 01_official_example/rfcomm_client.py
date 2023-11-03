#!/usr/bin/env python3
"""PyBluez simple example rfcomm-client.py

Simple demonstration of a client application that uses RFCOMM sockets intended
for use with rfcomm-server.

Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $
"""

import sys
import bluetooth

########################################################################
# Configure Service Info
########################################################################
service_uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_name = "SampleServer"

########################################################################
# Find Service
#   Optionally add python args in .vscode/launch.json
#    (in find_service, using specific bluetooth mac address as args can connect faster than using discover_devices)
########################################################################
addr = None
if len(sys.argv) < 2:
    print(
        f"No device specified. Searching for {service_name} from all nearby bluetooth devices..."
    )
else:
    addr = sys.argv[1]
    print(f"Searching for {service_name} on address {addr}...")

# search for the service
# (discover devices or search specific address, & only matched uuid will be showed)
service_matches = bluetooth.find_service(uuid=service_uuid, address=addr)

if len(service_matches) == 0:
    print(f"Couldn't find the {service_name} service.")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

if addr != None:
    for s in range(len(service_matches)):
        print("")
        print(f"service_matches: [{str(s)}]:")
        print(service_matches[s])
        print("")

print(f"Connecting to {name} through port {port} on address {host}...")

########################################################################
# Create the Client Socket
########################################################################
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))

########################################################################
# Send Messages
########################################################################
print("Connected. Type something:")
while True:
    data = input()
    if not data or data == "exit":
        break
    sock.send(data)

sock.close()
