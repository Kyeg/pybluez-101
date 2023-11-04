import bluetooth_service_info as bt_info

import bluetooth
import sys
import time

from u_ticket import generate_arbitrary_u_ticket
import u_ticket as u_ticket


######################################################
# JSON Generating
######################################################
def input_next_message() -> str:
    while True:
        print("")
        data_size: str = input("Sent U-Ticket with Data Size: ")

        if data_size == "exit":
            generated_u_ticket_str: str = "exit"
        else:
            try:
                generated_u_ticket_str: str = generate_json_message(int(data_size))
            except ValueError:  # ERROR: data_size cannot be converted to int
                continue
        break

    return generated_u_ticket_str


def generate_json_message(data_size: int) -> str:
    generated_request: dict = {
        "device_id": f"abcdef",
        "cmd_or_data": f"x" * data_size,
        "end_tag": f"END",
    }
    generated_u_ticket_str = generate_arbitrary_u_ticket(generated_request)

    return generated_u_ticket_str


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
        # Connection Socket: Connect to Device/Service
        ########################################################################
        print(f"+ Connecting to {name} through port {port} on address {host}...")
        self.connection_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.connection_socket.connect((host, port))
        print(f"+ Connection is generated with {host}.")

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

    def agent_loop(self):
        ########################################################################
        # Connection Socket: Send
        ########################################################################
        next_message = input_next_message()
        self.send_multiple_message(next_message)
        try:
            while True:
                ########################################################################
                # Connection Socket: Receive
                ########################################################################
                received_u_ticket_str: str = self.recv_multiple_message()

                # TODO: Contoller, e.g., input next message
                while True:
                    ########################################################################
                    # Connection Socket: Send
                    ########################################################################
                    next_message = input_next_message()
                    if next_message != "":
                        self.send_multiple_message(next_message)
                        break
        except OSError:
            print(f"Connection is closed by peer.")

    def close(self):
        ########################################################################
        # Socket: Closed
        ########################################################################
        self.connection_socket.close()
        print("Connection is closed.")


if __name__ == "__main__":
    ########################################################################
    # Bluetooth Service Lifecycle: Connect, Send, & Receive
    ########################################################################
    msg_sender = CustomizedMsgSender(
        service_uuid=bt_info.SERVICE_UUID,
        service_name=bt_info.SERVICE_NAME,
        reconnect_times=bt_info.RECONNECT_TIMES,
        reconnect_interval=bt_info.RECONNECT_INTERVAL,
    )
    msg_sender.connect()

    msg_sender.agent_loop()

    msg_sender.close()
