import socket
import threading

# Server configuration
HOST = '192.168.0.39'  # Localhost for testing, replace with actual IP if needed
PORT = 5000  # Port for the main server

# Set up data structures to manage clients and rooms
clients = {}  # Stores client sockets with their address as the key
rooms = {"main": set()}  # Dictionary of rooms, starting with a "main" room
room_addresses = {"main": ('224.1.1.1', 5004)}  # Multicast addresses for rooms

def handle_client(client_socket, addr):
    #Handles communication with a client
    current_room = "main"
    rooms[current_room].add(client_socket)

    print(f"Client {addr} connected to the main room.")
    try:
        while True:
            try:
                #receive messages from the client
                message = client_socket.recv(1024).decode('utf-8')
            
                #check if message is empty, indicating disconnections
                if not message:
                    print(f"Client {addr} disconnected.")
                    break

                print(f"Message from {addr} in {current_room}: {message}")

                # Check if the message is a room change request or standard message
                if message.startswith("/room "):
                    #spli command and check if room exists
                    parts = message.split(" ", 1)
                    if len(parts) > 1:
                        new_room = parts[1]
                        if new_room in rooms:
                            change_room(client_socket, addr, current_room, new_room)
                            current_room = new_room
                        else:
                            client_socket.send(f"Room {new_room} does not exist.".encode('utf-8'))
                    else:
                        client_socket.send("Invalid command. Use /room [room_name] to switch rooms.".encode('utf-8'))
                else:
                    #broadcast message to all clients in the room
                    broadcast_message(current_room, message, addr)
            
            except Exception as e:
                #catch & log specific exception but allow to continue
                print(f"Error receiving message from {addr}: {e}")
                continue # retry instead of breaking 

    except Exception as e:
        print (f"Unhandled error with client {addr}: {e}")
    finally:
        remove_client(client_socket, addr, current_room)

def change_room(client_socket, addr, current_room, new_room):
    #Moves a client from one room to another
    rooms[current_room].remove(client_socket)
    rooms[new_room].add(client_socket)
    client_socket.send(f"You have joined room: {new_room}".encode('utf-8'))
    print(f"Client {addr} moved from {current_room} to {new_room}")

def broadcast_message(room, message, addr):
    #Broadcasts a message to all clients in a room
    for client in rooms[room]:
        try:
            client.send(f"{addr}: {message}".encode('utf-8'))
        except:
            client.close()
            rooms[room].remove(client)

def remove_client(client_socket, addr, current_room):
    #Removes a client from the server and closes the socket.
    print(f"Removing client {addr} from {current_room}")
    client_socket.close()
    if client_socket in rooms[current_room]:
        rooms[current_room].remove(client_socket)
    if addr in clients:
        del clients[addr]

def start_server():
    #Main server function to accept connections
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
