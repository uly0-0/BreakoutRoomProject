import socket
import threading
import instructor
import student

class SystemServer:
    def __init__(self, host='0.0.0.0', port=5501): # use '0.0.0.0' for external connections
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows immediate reuse of port if restarting
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.lock = threading.Lock()
        
    def broadcast(self, message, sender):
        with self.lock:
            for client in self.clients:
                if client != sender:
                    try:
                        client.sendall(message)
                    except:
                        client.close()
                        self.clients.remove(client)
                        
    def handle_client(self, conn, addr):
        print(f"New connection: {addr}")
        self.clients.append(conn)
        
        while True:
            try:
                message = conn.recv(1024)
                if not message:
                    break
                self.broadcast(message, conn)
            except:
                break

        with self.lock:
            conn.close()
            self.clients.remove(conn)
        print(f"Connection closed: {addr}")
        
    def start(self):
        print("Server started")
        while True:
            conn, addr = self.server.accept()
            print(f"Connected to {addr}")
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = SystemServer()
    server.start()
