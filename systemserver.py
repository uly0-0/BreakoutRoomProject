import socket
import threading

# Server configuration
HOST = '129.8.203.100'  # Localhost for testing, replace with actual IP if needed
PORT = 5000  # Port for the main server

# Set up data structures to manage clients and rooms
clients = {}  # Stores client sockets with their address as the key
rooms = {
    "main": set(),
    "room1":{"clients": set(), "video": "room1_video.mp4"},
    "room2":{"clients": set(), "video": "room2_video.mp4"},
    "room3":{"clients": set(), "video": "room3_video.mp4"}

}  # Dictionary of rooms, starting with a "main" room and 3 additional rooms for separate videos
room_addresses = {
    "main": ('224.1.1.1', 5004),
    "room1": ('224.1.1.2', 5005),
    "room2": ('224.1.1.3', 5006),
    "room3": ('224.1.1.4', 5007)
}  # Multicast addresses for rooms

instructor_addr = None # address of the instructor
# need instructor address to be able to allow only instructor to move students to designated rooms


    
def handle_client(client_socket, addr):
    global instructor_addr
    # Request username and store it
    client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    clients[username] = client_socket

    #Handles communication with a client
    current_room = "main"
    rooms[current_room].add(client_socket)
    
    # Identify the instructor
    if instructor_addr is None:
        instructor_addr = addr
        client_socket.send("You are the instructor.".encode('utf-8'))
    else:
        client_socket.send("You are a student.".encode('utf-8'))
    
    print(f"Client {addr} connected as {username} in room {current_room}")

    try:
        while True:
            #receive messages from the client
            message = client_socket.recv(1024).decode('utf-8')
        
            #check if message is empty, indicating disconnections
            if not message:
                print(f"Client {username} disconnected.")
                break
            print(f"Message from {username} in {current_room}: {message}")
            if message.startswith("REQUEST_ROOM"):
                _, requested_room = message.split(" ", 1)
                notify_instructor_request(username, requested_room)
            elif addr == instructor_addr: #Check for instructor commands
                handle_instructor_command(message, client_socket, current_room)
            else:
                if message.startswith("/private"):
                    handle_private_message(message, client_socket)
                else:
                    broadcast_message(current_room, f"{username}: {message}", client_socket)

    except Exception as e:
        print(f"Error handling client {addr}: {e}")

def broadcast_message(room_name, message, sender_socket):
    #Broadcasts a message to all clients in a room
    if room_name in rooms:
        for client_socket in rooms[room_name]:
            if client_socket != sender_socket:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting message to {client_socket}: {e}")
                    
def notify_instructor_request(username, requested_room):
    if instructor_addr:
        instructor_socket = next((s for u, s in clients.items() if u == instructor_addr), None)
        if instructor_socket:
            instructor_socket.send(f"Student {username} requested room {requested_room}".encode('utf-8'))
    else:
        print(f"No instructor connected to handle request for {username}.")

# Handle commands from the isntructor
def handle_instructor_command(command, client_socket, current_room):
    parts = command.split()
    if not parts:
        return

    cmd = parts[0]
    if cmd == "/move_student":
        if len(parts) == 3:
            student_username = parts[1]
            room_name = parts[2]
            move_student(student_username, room_name)
            client_socket.send(f"Moved {student_username} to {room_name}".encode('utf-8'))

    elif cmd == "/play_video":
        if len(parts) == 2:
            room_name = parts[1]
            play_video(room_name)
            client_socket.send(f"Playing video in {room_name}".encode('utf-8'))

    elif cmd == "/list_connected_users":
        list_connected_users(client_socket)
    elif cmd == "/close_room":
        if len(parts) == 2:
            room_name = parts[1]
            close_room(room_name)
            client_socket.send(f"Closed room {room_name}".encode('utf-8'))

    elif cmd == "/create_room":
        if len(parts) == 2:
            room_name = parts[1]
            create_room(room_name)
            client_socket.send(f"Created room {room_name}".encode('utf-8'))

    elif cmd == "/list_rooms":
        list_rooms(client_socket)
    elif cmd == "/current_room":
        if len(parts) == 2:
            username = parts[1]
            current_room = get_current_room(username)
            if current_room:
                client_socket.send(f"{username} is in {current_room}".encode('utf-8'))
            else:
                client_socket.send(f"{username} is not in any room.".encode('utf-8'))
        else:
            current_room = get_current_room(username)
            client_socket.send(f"You are in {current_room}".encode('utf-8'))
    else:
        broadcast_message(current_room, command, client_socket)

def handle_private_message(command, sender_socket):
    parts = command.split(maxsplit=2)
    if len(parts) < 3:
        sender_socket.send("Invalid private message format. Use /private <user> <message>".encode('utf-8'))
        return

    _, target_username, private_message = parts
    if target_username in clients:
        target_socket = clients[target_username]
        try:
            target_socket.send(f"Private message from {get_username(sender_socket)}: {private_message}".encode('utf-8'))
            sender_socket.send(f"Private message sent to {target_username}".encode('utf-8'))
        except Exception as e:
            sender_socket.send(f"Failed to send private message to {target_username}: {e}".encode('utf-8'))
    else:
        sender_socket.send(f"User {target_username} not found.".encode('utf-8'))

def get_username(client_socket):
    for username, socket in clients.items():
        if socket == client_socket:
            return username
    return None
def get_current_room(username):
    for room, data in rooms.items():
        if username in data["clients"]:
            return room
    return None

def move_student(student_username, room_name):
    print(f"Attempting to move student: {student_username} to room: {room_name}")
    print(f"Current clients: {clients}")
    print(f"Current rooms: {rooms}")

    if student_username in clients:
        client_socket = clients[student_username]
        current_room = None
        for room_name_key, room in rooms.items():
            if isinstance(room, dict) and client_socket in room["clients"]:
                room["clients"].remove(student_username)
                current_room = room_name_key
                break
        if current_room:
            if room_name in rooms:
                rooms[room_name]["clients"].add(student_username)
                client_socket.send(f"You have been moved to room: {room_name}".encode('utf-8'))
            else:
                print(f"Room {room_name} not found.")
                rooms[current_room]["clients"].add(student_username)  # Re-add to the original room
        else:
            print(f"User {student_username} was not found in any room.")
    else:
        print(f"User {student_username} not found.")

#fix play video function
def play_video(room_name): #play video in a specified room
        return
#list connected users
def list_connected_users(client_socket):
     users = "\n".join([str(user) for user in clients.keys()])  
     client_socket.send(f"Connected users: \n {users}".encode('utf-8'))

#close room
def close_room(room_name):
    if room_name in rooms:
        # Create a list of clients to avoid modifying the set while iterating
        clients_to_move = list(rooms[room_name]["clients"])
        
        for client_socket in clients_to_move:
            #remove clien from the current room
            rooms[room_name]["clients"].remove(client_socket)
            rooms["main"].add(client_socket)
            client_socket.send(f"The room {room_name} has been closed. You have been moved to the main room.".encode('utf-8'))
        
        # Clear the room after moving all clients
        rooms[room_name]["clients"].clear()
        print(f"Room {room_name} has been closed and all clients have been moved to the main room.")
    else:
        print(f"Room {room_name} does not exist.")

#function to create a new room
def create_room(room_name):
    if room_name not in rooms:
        rooms[room_name] = set()
        room_addresses[room_name] = ('224.1.1.1', 5004)# multicast address might need to change
        print(f"Room {room_name} created")

# function to list all rooms
def list_rooms(client_socket):
    room_list = []
    for room_name, clients in rooms.items():
        room_list.append(f"{room_name}: {len(clients)} clients")
    room_list = "Available rooms: " + ", ".join(rooms.keys())
    client_socket.send(room_list.encode('utf-8'))

# function to change room
def change_room(client_socket, addr, current_room, new_room):
    #Moves a client from one room to another
    rooms[current_room].remove(client_socket)
    rooms[new_room].add(client_socket)
    client_socket.send(f"You have joined room: {new_room}".encode('utf-8'))
    print(f"Client {addr} moved from {current_room} to {new_room}")


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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Serving on {HOST}:{PORT}\n")
    print(f"waiting for connections...")
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        clients[addr] = client_socket
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
