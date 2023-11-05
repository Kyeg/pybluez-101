# Resource (Measurer)
from simple_measurer import (
    start_process_timer,
    get_process_time,
    start_comm_timer,
    get_comm_time,
    simple_size_calculator,
)


######################################################
# Measurement Helper:
#   Data Size + Process Response Time
######################################################
def measure_process_start() -> None:
    start_process_timer()


def measure_cli_process(cli_name: str) -> float:
    # Response Time
    process_time_xxx: float = get_process_time()

    # Print
    print(f"+ Receive UI Input: {cli_name}")
    print(f"process_time_xxx = {process_time_xxx:.4f} seconds")
    print(f"")


def measure_comm_process(comm_name: str) -> float:
    # Response Time
    process_time_xxx: float = get_process_time()

    # Print
    print(f"+ Receive Comm Input: {comm_name}")
    print(f"process_time_xxx = {process_time_xxx:.4f} seconds")
    print(f"")


######################################################
# Measurement Helper:
#   Comm Response Time
######################################################
def measure_comm_start() -> None:
    start_comm_timer()


def measure_comm_time(comm_name: str, received_message_json) -> float:
    # Data Size
    message_size_xxx: int = simple_size_calculator(received_message_json)

    # Response Time
    comm_time_xxx: float = get_comm_time()

    # Print
    print(f"+ Receive Comm Input: {comm_name}")
    # print(f"+ Received Message: {received_message_json}")
    print(f"message_size_xxx = {message_size_xxx} bytes")
    print(f"comm_time_xxx = {comm_time_xxx:.4f} seconds")
    print(f"")
