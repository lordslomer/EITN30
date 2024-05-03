import socket 
socket_addr = '10.0.0.1'
socket_port = 12739
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind((socket_addr,socket_port))
print(f"listening at {socket_port}")

try:
    while True:
        message, _ = socket_server.recv(32)
        print(message)

        # Send a response
        # response = f"Echo: {message.decode()}"
        # socket_server.sendto(response.encode(), client_address)

except KeyboardInterrupt:
    socket_server.close()
    print("Server shutdown.")
