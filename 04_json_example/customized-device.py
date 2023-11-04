import bluetooth_service_info as bluetooth_service_info

import bluetooth


######################################################
# Data Size Measurement
######################################################
def simple_size_calculator(message: str) -> int:
    return len(message.encode("utf-8"))


class CustomizedMsgReceiver:
    def __init__(self, service_uuid, service_name):
        ########################################################################
        # Configure Service Info
        ########################################################################
        self.service_uuid = service_uuid
        self.service_name = service_name

        ########################################################################
        # Sockets
        ########################################################################
        self.accept_socket = None
        self.connection_socket = None

    def accept(self) -> str:
        ########################################################################
        # Accept Socket: Open Advertise Service
        ########################################################################
        self.accept_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.accept_socket.bind(("", bluetooth.PORT_ANY))
        self.accept_socket.listen(1)
        service_port = self.accept_socket.getsockname()[1]

        bluetooth.advertise_service(
            self.accept_socket,
            self.service_name,
            service_id=self.service_uuid,
            service_classes=[self.service_uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
            # protocols=[bluetooth.OBEX_UUID]
        )

        ########################################################################
        # Connection Socket: Created through Server Socket
        ########################################################################
        print(f"+ Waiting for connection on RFCOMM port {service_port}...")
        self.connection_socket, client_info = self.accept_socket.accept()
        print(f"+ Connection is generated with {client_info}.")

    def recv_message(self) -> str:
        ########################################################################
        # Connection Socket: Receive
        ########################################################################
        received_message: bytes = self.connection_socket.recv(1024)
        received_message_str: str = received_message.decode("UTF-8")

        print("")
        print(f"Received Message: {received_message_str}")
        print(f"Size = {simple_size_calculator(received_message_str)} bytes")

        return received_message_str

    def send_message(self, sent_message: str):
        ########################################################################
        # Connection Socket: Send
        ########################################################################
        print("")
        print(f"Sent Message: {sent_message}")
        print(
            f"Size = {simple_size_calculator(sent_message)} bytes (Cannot exceed about 1024 bytes)"
        )

        self.connection_socket.send(sent_message)

    def device_loop(self):
        try:
            while True:
                ########################################################################
                # Connection Socket: Receive
                ########################################################################
                received_u_ticket_str: str = self.recv_message()
                if received_u_ticket_str == "exit":
                    break

                # TODO: Contoller, e.g., echo the message
                generated_r_ticket_str: str = f"R|||{received_u_ticket_str}|||"

                ########################################################################
                # Connection Socket: Send
                ########################################################################
                self.send_message(generated_r_ticket_str)
        except OSError:
            print(f"+ Connection is closed by peer.")

    def close(self):
        ########################################################################
        # Sockets: Closed
        ########################################################################
        self.connection_socket.close()
        self.accept_socket.close()
        print("+ Connection is closed.")


if __name__ == "__main__":
    ########################################################################
    # Bluetooth Service Lifecycle: Accept, Receive, & Send
    ########################################################################
    msg_receiver = CustomizedMsgReceiver(
        service_uuid=bluetooth_service_info.SERVICE_UUID,
        service_name=bluetooth_service_info.SERVICE_NAME,
    )
    peer_address = msg_receiver.accept()

    msg_receiver.device_loop()

    msg_receiver.close()
