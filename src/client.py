import socket  # Importing the socket module for network communication
import struct  # Importing struct module for packing and unpacking binary data

def send_operation(operation, operand1, operand2):
    """
    Sends an arithmetic operation to a server, receives the result, and returns it.

    Args:
    operation (str): The operation to perform ('+', '-', '*', '/', '!' to exit).
    operand1 (int): The first operand for the operation.
    operand2 (int): The second operand for the operation.

    Returns:
    int or None: Result of the operation if successful, None if '!' is sent to exit.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket
    client_socket.connect(('localhost', 12345))  # Connecting to server on localhost, port 12345
    
    if operation == '!':
        # Send a special signal to indicate closure
        client_socket.sendall(b'!')
        client_socket.close()
        return None  # No result to return
    
    packed_data = struct.pack('!cii', operation.encode(), operand1, operand2)  # Packing operation and operands into binary data
    client_socket.sendall(packed_data)  # Sending packed data to server
    
    result_data = client_socket.recv(4)  # Receiving result data from server
    result = struct.unpack('!i', result_data)[0]  # Unpacking received data to get the result
    client_socket.close()  # Closing the connection with the server
    
    return result  # Returning the result of the operation

if __name__ == "__main__":
    while True:
        operation = input("Enter operation (+, -, *, /, ! to exit): ")
        if operation == '!':
            print("Exiting...")
            break
        
        if operation not in ['+', '-', '*', '/']:
            print("Unsupported operation.")
            continue
        
        operand1 = int(input("Enter first operand: "))
        operand2 = int(input("Enter second operand: "))
        
        result = send_operation(operation, operand1, operand2)  # Calling send_operation to perform the operation
        if result is not None:
            print(f"The result is: {result}")  # Displaying the result if it's not None