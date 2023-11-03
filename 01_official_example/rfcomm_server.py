#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $
"""

import bluetooth


########################################################################
# Configure Service Info
########################################################################
service_uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_name = "SampleServer"

########################################################################
# Open Advertise Service
########################################################################
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
service_port = server_sock.getsockname()[1]

bluetooth.advertise_service(
    server_sock,
    service_name,
    service_id=service_uuid,
    service_classes=[service_uuid, bluetooth.SERIAL_PORT_CLASS],
    profiles=[bluetooth.SERIAL_PORT_PROFILE],
    # protocols=[bluetooth.OBEX_UUID]
)


########################################################################
# Wait for Connection
########################################################################
print(f"Waiting for connection on RFCOMM port {service_port}")

client_sock, client_info = server_sock.accept()
print(f"Accepted connection from {client_info}")


########################################################################
# Receive Messages
########################################################################
try:
    while True:
        data = client_sock.recv(1024)
        if not data or data == "exit":
            break
        print(f"Received: {data}")
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
