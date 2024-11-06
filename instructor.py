import socket

class Instructor:
    def __init__(self, host='localhost', port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
    def send_message(self, message):
        self.client.sendall(message.encode('utf-8'))
        
    def start(self):
        print("Instructor connected")
        while True:
            message = input("Enter message: ")
            self.send_message(f"Instructor: {message}")
            
if __name__ == "__main__":
    instructor = Instructor()
    instructor.start()
