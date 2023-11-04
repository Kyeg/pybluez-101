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
        # Socket
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
        # Recv Socket: Created through Server Socket
        ########################################################################
        print(f"+ Waiting for connection on RFCOMM port {service_port}...")
        self.connection_socket, client_info = self.accept_socket.accept()
        print(f"+ Connection is generated with {client_info}.")

    def recv_loop(self):
        ########################################################################
        # Recv Socket: Receive Messages
        ########################################################################
        try:
            while True:
                received_u_ticket_byte: bytes = self.connection_socket.recv(1024)
                received_u_ticket_str: str = received_u_ticket_byte.decode("UTF-8")
                print("")
                print(f"Received U-Ticket: {received_u_ticket_str}")
                print(
                    f"Size of received_u_ticket_str = {simple_size_calculator(received_u_ticket_str)} bytes"
                )
                if received_u_ticket_str == "exit":
                    break

                # TODO: Contoller, e.g., echo the message
                generated_r_ticket_str: str = f"R|||{received_u_ticket_str}|||"
                print("")
                print(f"Sent R-Ticket: {generated_r_ticket_str}")
                print(
                    f"Size of generated_r_ticket_str = {simple_size_calculator(generated_r_ticket_str)} bytes (Cannot exceed about 1024 bytes)"
                )
                self.connection_socket.send(generated_r_ticket_str)
        except OSError:
            print(f"+ Connection is closed by peer.")

    def close(self):
        ########################################################################
        # Recv Socket: Closed
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

    msg_receiver.recv_loop()

    msg_receiver.close()
