import bluetooth_service as bt_service
from bluetooth_service import ConnectingWorker, ConnectionSocket

from u_ticket import generate_arbitrary_u_ticket


######################################################
# JSON Generating
######################################################
def input_next_message() -> str:
    while True:
        print("")
        data_content: str = input("Set Data in U-Ticket: ")
        data_size: str = input("Set Data Size (x N): ")

        if data_content == "exit":
            generated_u_ticket_str: str = "exit"
        else:
            try:
                generated_u_ticket_str: str = generate_json_message(
                    data_content, int(data_size)
                )
            except ValueError:  # ERROR: data_size cannot be converted to int
                continue
        break

    return generated_u_ticket_str


def generate_json_message(data_content: str, data_size: int) -> str:
    generated_request: dict = {
        "device_id": f"abcdef",
        "cmd_or_data": f"{data_content}" * data_size,
        "end_tag": f"END",
    }
    generated_u_ticket_str = generate_arbitrary_u_ticket(generated_request)

    return generated_u_ticket_str


def agent_event_loop(connection_socket: ConnectionSocket):
    ########################################################################
    # Connection Socket: Send
    ########################################################################
    next_message = input_next_message()
    connection_socket.send_message(next_message)
    try:
        while True:
            ########################################################################
            # Connection Socket: Receive
            ########################################################################
            received_u_ticket_str: str = connection_socket.recv_message()

            # TODO: Contoller, e.g., input next message
            while True:
                ########################################################################
                # Connection Socket: Send
                ########################################################################
                next_message = input_next_message()
                if next_message != "":
                    connection_socket.send_message(next_message)
                    break
    except OSError:
        print(f"Connection is closed by peer.")


if __name__ == "__main__":
    ########################################################################
    # Bluetooth Service Lifecycle: Connect New Connection
    ########################################################################
    connecting_socket = ConnectingWorker(
        service_uuid=bt_service.SERVICE_UUID,
        service_name=bt_service.SERVICE_NAME,
        reconnect_times=bt_service.RECONNECT_TIMES,
        reconnect_interval=bt_service.RECONNECT_INTERVAL,
    )
    connection_socket = connecting_socket.connect()

    ########################################################################
    # Bluetooth Service Lifecycle: Receive & Send in Connection
    ########################################################################
    agent_event_loop(connection_socket)

    ########################################################################
    # Bluetooth Service Lifecycle: Close Connection
    ########################################################################
    connection_socket.close()
