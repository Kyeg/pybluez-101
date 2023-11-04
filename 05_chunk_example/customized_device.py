import bluetooth_service_info as bt_info

import bluetooth
import time


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

    def _byte_backto_str(self, message_byte: bytes) -> str:
        return message_byte.decode("UTF-8")

    def _message_size(self, message: str) -> int:
        return len(message.encode("UTF-8"))

    def recv_multiple_message(self) -> str:
        received_chunk_strs = []
        bytes_received = 0
        message_length = str(bt_info.MSG_MAX_SIZE)
        while bytes_received < int(message_length):
            # Receive
            chunk_with_length: bytes = self.connection_socket.recv(
                bt_info.COMM_BUFFER_SIZE
            )
            chunk_with_length_str: str = self._byte_backto_str(chunk_with_length)
            print("")
            print(f"Received Chunk With Length: {chunk_with_length_str}")

            # Combined Chunks into Message
            message_length = chunk_with_length_str.split(bt_info.SPLIT_SIGN)[0]
            # print(f"Message Length: {message_length}")
            received_chunk_str = chunk_with_length_str.split(bt_info.SPLIT_SIGN)[1]
            # print(f"Received Chunk: {received_chunk_str}")
            received_chunk_strs.append(received_chunk_str)
            bytes_received = bytes_received + self._message_size(received_chunk_str)

        # Combined Chunks into Message
        original_message_str = ""
        for received_chunk_str in received_chunk_strs:
            original_message_str += received_chunk_str
        print("")
        print(f"Received Message: {original_message_str}")

        return original_message_str

    def send_multiple_message(self, original_message_str: str):
        # Combined Message
        print("")
        print(f"Sent Message: {original_message_str}")

        # Divide message into Chunks
        message_length = self._message_size(original_message_str)
        print(f"Message Length: {message_length}")
        sent_chunk_strs = []
        for i in range(0, len(original_message_str), bt_info.MSG_MAX_SIZE):
            sent_chunk_str = original_message_str[i : i + bt_info.MSG_MAX_SIZE]
            sent_chunk_strs.append(sent_chunk_str)

        for sent_chunk_str in sent_chunk_strs:
            message_with_length = (
                f"{message_length}{bt_info.SPLIT_SIGN}{sent_chunk_str}"
            )
            # print(f"Sent Chunk: {sent_chunk_str}")
            # print(f"Sent Chunk With Length: {message_with_length}")

            # Send
            self.connection_socket.send(message_with_length)
            time.sleep(bt_info.WAIT_NEXT_CHUNK)

    def device_loop(self):
        try:
            while True:
                ########################################################################
                # Connection Socket: Receive
                ########################################################################
                received_u_ticket_str: str = self.recv_multiple_message()
                if received_u_ticket_str == "exit":
                    break

                # TODO: Contoller, e.g., echo the message
                generated_r_ticket_str: str = f"R|||{received_u_ticket_str}|||"

                ########################################################################
                # Connection Socket: Send
                ########################################################################
                self.send_multiple_message(generated_r_ticket_str)
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
        service_uuid=bt_info.SERVICE_UUID,
        service_name=bt_info.SERVICE_NAME,
    )
    peer_address = msg_receiver.accept()

    msg_receiver.device_loop()

    msg_receiver.close()
