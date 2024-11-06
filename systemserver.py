import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost for testing, replace with actual IP if needed
PORT = 12345  # Port for the main server

# Set up data structures to manage clients and rooms
clients = {}  # Stores client sockets with their address as the key
rooms = {"main": set()}  # Dictionary of rooms, starting with a "main" room
room_addresses = {"main": ('224.1.1.1', 5004)}  # Multicast addresses for rooms

def handle_client(client_socket, addr):
    """Handles communication with a client."""
    current_room = "main"
    rooms[current_room].add(client_socket)

    print(f"Client {addr} connected to the main room.")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Message from {addr} in {current_room}: {message}")

                # Check if the message is a room change request or standard message
                if message.startswith("/room "):
                    new_room = message.split(" ")[1]
                    if new_room in rooms:
                        change_room(client_socket, addr, current_room, new_room)
                        current_room = new_room
                    else:
                        client_socket.send(f"Room {new_room} does not exist.".encode('utf-8'))
                else:
                    broadcast_message(current_room, message, addr)
            else:
                break
    except:
        print(f"Client {addr} disconnected.")
    finally:
        remove_client(client_socket, addr, current_room)

def change_room(client_socket, addr, current_room, new_room):
    """Moves a client from one room to another."""
    rooms[current_room].remove(client_socket)
    rooms[new_room].add(client_socket)
    client_socket.send(f"You have joined room: {new_room}".encode('utf-8'))
    print(f"Client {addr} moved from {current_room} to {new_room}")

def broadcast_message(room, message, addr):
    """Broadcasts a message to all clients in a room."""
    for client in rooms[room]:
        try:
            client.send(f"{addr}: {message}".encode('utf-8'))
        except:
            client.close()
            rooms[room].remove(client)

def remove_client(client_socket, addr, current_room):
    """Removes a client from the server and closes the socket."""
    print(f"Removing client {addr} from {current_room}")
    client_socket.close()
    if client_socket in rooms[current_room]:
        rooms[current_room].remove(client_socket)
    if addr in clients:
        del clients[addr]

def start_server():
    """Main server function to accept connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server started, waiting for connections...")
    while True:
        client_socket, addr = server_socket.accept()
        clients[addr] = client_socket
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
