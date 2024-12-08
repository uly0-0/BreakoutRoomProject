import socket
import threading

class Student:
    def __init__(self, host='192.168.0.39', port=5000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message)
            except:
                print("Connection lost")
                self.client.close()
                break
                
    def send_message(self, message):
        self.client.sendall(message.encode('utf-8'))
        
    def start(self):
        print("Student connected")
        threading.Thread(target=self.receive_messages).start()
        
        while True:
            message = input("Enter message: ")
            self.send_message(f"Student: {message}")
            
if __name__ == "__main__":
    student = Student()
    student.start()
