# Resource (Comm)
import bluetooth_service as bt_service
from bluetooth_service import AcceptSocket, ConnectionSocket

# Resource (Measurer)
from measure_executor import (
    measure_process_start,
    measure_cli_process,
    measure_comm_process,
    measure_comm_start,
    measure_comm_time,
)


def device_event_loop(connection_socket: ConnectionSocket):
    try:
        while True:
            ########################################################################
            # Connection Socket: Receive
            ########################################################################
            received_u_ticket_str: str = connection_socket.recv_message()
            if received_u_ticket_str == "exit":
                break

            # TODO: Contoller, e.g., echo the message
            # Start Process Measurement
            measure_process_start()
            generated_r_ticket_str: str = f"R<<<{received_u_ticket_str}>>>"
            # End Process Measurement
            measure_comm_process("device_recv_u_ticket")

            ########################################################################
            # Connection Socket: Send
            ########################################################################
            connection_socket.send_message(generated_r_ticket_str)
    except OSError:
        print(f"+ Connection is closed by peer.")


if __name__ == "__main__":
    ########################################################################
    # Bluetooth Service Lifecycle: Accept New Connection
    ########################################################################
    accept_socket = AcceptSocket(
        service_uuid=bt_service.SERVICE_UUID,
        service_name=bt_service.SERVICE_NAME,
    )
    connecting_socket = accept_socket.accept()

    ########################################################################
    # Bluetooth Service Lifecycle: Receive & Send in Connection
    ########################################################################
    device_event_loop(connecting_socket)

    ########################################################################
    # Bluetooth Service Lifecycle: Close Connection
    ########################################################################
    connecting_socket.close()

    ########################################################################
    # Bluetooth Service Lifecycle: Stop Accepting New Connections
    ########################################################################
    accept_socket.close()
