import socket
import threading

# Instructor program configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

class Instructor: # instructor class
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    
    def receive_message(self):
        #Receives incoming messages from the server."""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")
            except:
                print("Connection lost")
                self.client.close()
                break

    def send_message(self):
        #Handles outgoing messages from the instructor."""
        while True:
            message = input("Enter command (e.g., /room [room_name], /assign [student_addr] [room]): , /create_room [room_name], /list_rooms): ")
            self.client.sendall(message.encode('utf-8'))
        
    def start(self): # student connects 
        print("Instructor connected") 
        thread_send = threading.Thread(target=self.send_message)
        thread_receive = threading.Thread(target=self.receive_message)
        thread_send.start()
        thread_receive.start()

        # Wait for threads to complete
        thread_send.join()
        thread_receive.join()
        self.client.close()
      

if __name__ == "__main__":
    instructor = Instructor()
    instructor.start()
