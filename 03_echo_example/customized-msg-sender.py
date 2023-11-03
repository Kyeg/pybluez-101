import bluetooth_service_info as bluetooth_service_info

import bluetooth
import sys
import time


class CustomizedMsgSender:
    def __init__(self, service_uuid, service_name, reconnect_times, reconnect_interval):
        ########################################################################
        # Configure Service Info
        ########################################################################
        self.service_uuid = service_uuid
        self.service_name = service_name

        ########################################################################
        # Socket
        ########################################################################
        self.connection_socket = None
        self.reconnect_times = reconnect_times
        self.reconnect_interval = reconnect_interval

    def connect(self):
        ########################################################################
        # Service Discovery Protocol (SDP): Find Device/Service
        #   Optionally add python args in .vscode/launch.json
        #     (in find_service, using specific bluetooth mac address as args can connect faster than using discover_devices)
        ########################################################################
        addr = None
        if len(sys.argv) < 2:
            print(
                f"+ No device specified. Searching for {self.service_name} from all nearby bluetooth devices..."
            )
        else:
            addr = sys.argv[1]
            print(f"+ Searching for {self.service_name} on address {addr}...")

        # Search for the service
        #   Discover devices or search specific address, & only matched uuid will be showed
        #   Reconnect n times every m seconds
        for reconnect_num in range(1, 1 + self.reconnect_times):
            service_matches = bluetooth.find_service(
                uuid=self.service_uuid,
                address=addr,
            )
            if len(service_matches) == 0:
                print(
                    f"+ Re-connecting {self.service_name} services : {reconnect_num} attempt"
                )
                time.sleep(self.reconnect_interval)
            else:
                break

        if len(service_matches) == 0:
            raise RuntimeError(f"+ Couldn't find the {self.service_name} service.")
        else:
            first_match = service_matches[0]
            port = first_match["port"]
            name = first_match["name"]
            host = first_match["host"]

        ########################################################################
        # Sender Socket: Connect to Device/Service
        ########################################################################
        print(f"+ Connecting to {name} through port {port} on address {host}...")
        self.connection_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.connection_socket.connect((host, port))
        print(f"+ Connection is generated with {host}.")

    def recv_loop(self):
        ########################################################################
        # Recv Socket: Receive Messages
        ########################################################################
        try:
            while True:
                data_byte: bytes = self.connection_socket.recv(1024)
                data_str: str = data_byte.decode("UTF-8")
                print(f"Received: {data_str}")

                # TODO: Contoller, e.g., input next message
                while True:
                    next_message: str = input("Sent U-Ticket: ")
                    if next_message != "":
                        self.connection_socket.send(next_message)
                        break
        except OSError:
            print(f"Connection is closed by peer.")

    def send_data(self, data: str):
        ########################################################################
        # Sender Socket: Send Messages
        ########################################################################
        self.connection_socket.send(data)

    def close(self):
        ########################################################################
        # Sender Socket: Closed
        ########################################################################
        self.connection_socket.close()
        print("Connection is closed.")


if __name__ == "__main__":
    ########################################################################
    # Bluetooth Service Lifecycle: Connect, Send, & Receive
    ########################################################################
    msg_sender = CustomizedMsgSender(
        service_uuid=bluetooth_service_info.SERVICE_UUID,
        service_name=bluetooth_service_info.SERVICE_NAME,
        reconnect_times=bluetooth_service_info.RECONNECT_TIMES,
        reconnect_interval=bluetooth_service_info.RECONNECT_INTERVAL,
    )
    msg_sender.connect()

    next_message: str = input("Sent U-Ticket: ")
    msg_sender.send_data(next_message)

    msg_sender.recv_loop()

    msg_sender.close()
