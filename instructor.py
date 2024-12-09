import socket
import threading

# Instructor program configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def send_message(sock):
    #Handles outgoing messages from the instructor."""
    while True:
        message = input("Enter command (e.g., /room [room_name], /assign [student_addr] [room]): , /create_room [room_name], /list_rooms): ")
        sock.send(message.encode('utf-8'))

def receive_message(sock):
    #Receives incoming messages from the server."""
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(f"Received: {message}")
            else:
                break
        except:
            break

def main():
    #Main function to connect to the server and handle input/output."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print("Instructor connected to the server.")

    # Start threads to send and receive messages
    thread_send = threading.Thread(target=send_message, args=(sock,))
    thread_receive = threading.Thread(target=receive_message, args=(sock,))
    thread_send.start()
    thread_receive.start()

    # Wait for threads to complete
    thread_send.join()
    thread_receive.join()
    sock.close()

if __name__ == "__main__":
    main()
