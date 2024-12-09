import socket
import threading

class Student: # student class 
    def __init__(self, host='127.0.0.1', port=5000): # Connecting to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                print(message) #recieve messages and decrypt from utf-8 decryption
            except:
                print("Connection lost") # If message cannot be receive connection lost 
                self.client.close()
                break
                
    def send_message(self, message):
        self.client.sendall(message.encode('utf-8')) # send a message and decode it utf-8
        
    def start(self): # student connects 
        print("Student connected") 
        threading.Thread(target=self.receive_messages).start()
        
        while True:
            message = input("Enter message: ") # Student enters a message 
            self.send_message(f"Student: {message}")
            
if __name__ == "__main__":
    student = Student() 
    student.start()
