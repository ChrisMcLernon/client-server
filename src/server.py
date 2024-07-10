import socket  # Importing the socket module for network communication
import struct  # Importing struct module for packing and unpacking binary data

MAX_INT = 2**31 - 1  # Maximum integer value for 32-bit signed integer

def perform_operation(operation, operand1, operand2, addr):
    """
    Performs a mathematical operation based on the given operation and operands.

    Args:
    operation (bytes): The operation to perform (+, -, *, /).
    operand1 (int): The first operand.
    operand2 (int): The second operand.
    addr (tuple): Address of the client.

    Returns:
    int: Result of the operation.

    Raises:
    ValueError: If operands are too large or if the result would cause overflow.
    """
    if abs(operand1) > MAX_INT or abs(operand2) > MAX_INT:
        raise ValueError("Operands are too large")
    
    if operation == b'+':
        result = operand1 + operand2
    elif operation == b'-':
        result = operand1 - operand2
    elif operation == b'*':
        result = operand1 * operand2
    elif operation == b'/':
        result = operand1 // operand2  # Integer division
    else:
        raise ValueError("Unsupported operation")
    
    if abs(result) > MAX_INT:
        raise ValueError("Result is too large and will cause overflow")
    
    return result

def start_server():
    """
    Starts a TCP server that performs arithmetic operations based on client requests.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket
    server_socket.bind(('localhost', 12345))  # Binding the socket to localhost on port 12345
    server_socket.listen(1)  # Listening for incoming connections, queueing up to 1 client
    print("Server is listening on port 12345")

    while True:
        conn, addr = server_socket.accept()  # Accepting a connection from a client
        print(f"Connected by {addr}")
        
        data = conn.recv(9)  # Receiving 9 bytes of data from the client
        if len(data) == 9:
            operation, operand1, operand2 = struct.unpack('!cii', data)  # Unpacking binary data into operation and operands
            try:
                result = perform_operation(operation, operand1, operand2, addr)  # Performing the requested operation
                conn.sendall(struct.pack('!i', result))  # Sending the result back to the client
            except ValueError as e:
                conn.sendall(struct.pack('!i', 0))  # Sending an error indication back to the client
                print(f"Error: {e}")
                
        print(f"Connection closed with {addr}")
        conn.close()  # Closing the connection with the client

if __name__ == "__main__":
    start_server()  # Starting the server if this script is run directly