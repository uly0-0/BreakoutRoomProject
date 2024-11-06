import socket
import select
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost for testing, replace with actual IP if needed
PORT = 12345  # Port for the main server

# Set up a dictionary to hold connected clients
clients = {}

# Multicast group details
MULTICAST_GROUP = ('224.1.1.1', 5004)

def handle_client(client_socket, addr):
    print(f"Client {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message from {addr}: {message}")

            # Broadcast message to other clients in the main room
            for client in clients.values():
                if client != client_socket:
                    client.send(f"{addr}: {message}".encode('utf-8'))
        except:
            break
    # Remove client if disconnected
    print(f"Client {addr} disconnected.")
    client_socket.close()
    del clients[addr]

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        clients[addr] = client_socket
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
