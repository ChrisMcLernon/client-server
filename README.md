# client-server

 ###### Example Client Server relationship

## client.py

`client.py` is a client-side script that connects to a server to perform arithmetic operations. It sends the operation and operands to the server, receives the result, and displays it to the user.

### Functions

`send_operations(operation, operand1, operand2)`

Sends an arithmetic operation to a server, receives the result, and returns it.

#### Args:
- `operation` (str): The operation to perform ('+', '-', '*', '/', '!' to exit).
- `operand1` (float): The first operand for the operation.
- `operand2` (float): The second operand for the operation.

#### Returns:
- `float` or `int`: Result of the operation if successful, rounded to 4 decimal places or converted to an integer if the result is an integer.

#### Example Usage:
```sh
result = send_operations('+', 5.0, 3.0)
print(result)  # Output: 8

result = send_operations('+', 5.1, 3.0)
print(result)  # Output: 8.1
```

### Main Execution
The main execution block runs an infinite loop that:

Prompts the user to enter an arithmetic operation (+, -, *, /, ! to exit).
If the user enters !, the program exits.
If the user enters an unsupported operation, it prints an error message and continues.
Prompts the user to enter two operands.
Calls send_operations with the entered operation and operands.
Prints the result of the operation.
Handles any exceptions that occur during input or operation processing.

### Example Usage:
```sh
$ python client.py
Enter operation (+, -, *, /, ! to exit): +
Enter first operand: 5
Enter second operand: 3
Result: 8
Enter operation (+, -, *, /, ! to exit): +
Enter first operand: 5.1
Enter second operand: 3
Result: 8.1
Enter operation (+, -, *, /, ! to exit): !
Exiting...
```

### Dependencies
socket: For creating a client socket to connect to the server.
struct: For packing and unpacking data to be sent and received over the network.
Error Handling
Catches and prints exceptions that occur during input or operation processing.

## server.py

`server.py` is a server-side script that sets up a TCP server to perform arithmetic operations based on client requests. It listens for incoming client connections, processes the requests, and sends back the results.

### Functions

#### `handle_client(conn, addr)`

Handles the communication with a connected client. It receives the operation and operands from the client, performs the operation, and sends back the result.

#### Args:
- `conn` (socket): The client connection socket.
- `addr` (tuple): Address of the client.

#### Process:
1. Logs the connection from the client.
2. Sets a timeout for the connection.
3. Receives data from the client.
4. Checks if the received data length matches the expected length for float operations.
5. Unpacks the received data to extract the operation and operands.
6. Performs the operation using `perform_operation`.
7. Sends the result back to the client.
8. Handles any errors during unpacking or operation processing by logging the error and sending `NaN` as the result.
9. Closes the connection.

#### `start_server(host, port)`

Starts a TCP server that listens for client connections and spawns a new thread to handle each client.

#### Args:
- `host` (str): The hostname or IP address to bind the server to.
- `port` (int): The port number to bind the server to.

#### Process:
1. Configures logging to the INFO level.
2. Creates a TCP socket.
3. Binds the socket to the specified host and port.
4. Starts listening for incoming connections.
5. Logs that the server has started.
6. Accepts incoming connections in an infinite loop.
7. For each connection, spawns a new thread to handle the client using `handle_client`.

### Main Execution

The main execution block starts the server on `localhost` at port `12345`.

#### Example Usage:
```sh
$ python server.py
INFO:root:Server started on localhost:12345
INFO:root:Connected by ('127.0.0.1', 54321)
INFO:root:Connection closed with ('127.0.0.1', 54321)
```

### Dependencies
socket: For creating server and client sockets.
struct: For packing and unpacking data to be sent and received over the network.
logging: For logging information and errors.
threading: For handling multiple client connections concurrently.
Error Handling
Logs errors related to struct unpacking and operation processing.
Sends NaN as the result to the client in case of errors.
