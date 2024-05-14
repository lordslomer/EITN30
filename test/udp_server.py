import socket

SERVER_ADDR = '10.0.0.1'  # Listen on all interfaces
PORT = 12739
BUFFER_SIZE = 1448

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_ADDR, PORT))
    print(f"Server listening on {SERVER_ADDR}:{PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        if data:
            sock.sendto(data, addr)  # Send acknowledgment

if __name__ == '__main__':
    run_server()
