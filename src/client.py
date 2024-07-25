import socket
import struct

def send_operations(operation, operand1,operand2):
    """
    Sends an arithmetic operation to a server, receives the result, and returns it.

    Args:
    operation (str): The operation to perform ('+', '-', '*', '/', '!' to exit).
    operand1 (float): The first operand for the operation.
    operand2 (float): The second operand for the operation.

    Returns:
    float or int: Result of the operation if successful rounded or integer if result is an integer.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 12345))

        packed_data = struct.pack('!cdd', operation.encode(), operand1, operand2)
        client_socket.sendall(packed_data)

        result = client_socket.recv(8)
        result = struct.unpack('!d', result)[0]

        formatted_result = round(result, 4)

        return int(formatted_result) if formatted_result.is_integer() else formatted_result

if __name__ == "__main__":
    while True:
        operation = input("Enter operation (+, -, *, /, ! to exit): ").strip()
        if operation == '!':
            print("Exiting...")
            break

        if operation not in ['+', '-', '*', '/']:
            print("Unsupported operation.")
            continue

        try:
            operand1 = float(input("Enter first operand: ").strip())

            operand2 = float(input("Enter second operand: ").strip())
        
            result = send_operations(operation, operand1, operand2)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
            continue