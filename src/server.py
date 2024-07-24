import socket
import struct
import logging
import threading

def perform_operation(operation, operand1, operand2):
    operations = {
        b'+': lambda x, y: x + y,
        b'-': lambda x, y: x - y,
        b'*': lambda x, y: x * y,
        b'/': lambda x, y: x / y if y != 0 else float('inf'),
    }

    if operation in operations:
        return operations[operation](operand1, operand2)
    else:
        raise ValueError("Unsupported operation")

def handle_client(conn, addr):
    logging.info(f"Connected by {addr}")
    conn.settimeout(5)
    try:
        data = conn.recv(17)
        
        if len(data) != 17:
                logging.error("Received data length does not match expected length for float operations")
                return
            
        try:
            operation, operand1, operand2 = struct.unpack('!cdd', data)
            result = perform_operation(operation, operand1, operand2)
            conn.sendall(struct.pack('!d', result))
        except struct.error as e:
            logging.error(f"Struct unpack error: {e}")
            conn.sendall(struct.pack('!d', float('nan')))
        except ValueError as e:
            logging.error(f"Operation error: {e}")
            conn.sendall(struct.pack('!d', float('nan')))
        
        logging.info(f"Connection closed with {addr}")
    finally:
        conn.close()

def start_server(host, port):
    logging.basicConfig(level=logging.INFO)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(host, port)
    server_socket.listen(5)
    logging.info(f"Server started on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server('localhost', 12345)