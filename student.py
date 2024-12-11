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
                if message:
                    print(f"Received: {message}") #recieve messages and decrypt from utf-8 decryption

            except:
                print("Connection lost") # If message cannot be receive connection lost 
                self.client.close()
                break
                
    def send_message(self):
        while True:
            message = input("Enter message: ") # input message
            self.client.sendall(message.encode('utf-8')) # send a message and decode it utf-8
        
    def start(self): # student connects 
        print("Student connected") 
        thread_send = threading.Thread(target=self.send_message)
        thread_receive = threading.Thread(target=self.receive_messages)
        thread_send.start()
        thread_receive.start()

        # Wait for threads to complete
        thread_send.join()
        thread_receive.join()
        self.client.close()

if __name__ == "__main__":
    student = Student() 
    student.start()
