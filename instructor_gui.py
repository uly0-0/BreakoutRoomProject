import tkinter as tk
from tkinter import messagebox
import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

class InstructorClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Instructor Client")
        self.root.geometry("400x300")
        
        # Connection status
        self.connected = False
        self.client_socket = None

        # GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(self.root, text="Instructor Client", font=("Arial", 16))
        title_label.pack(pady=10)

        # Message display area
        self.message_box = tk.Text(self.root, height=10, width=40, state="disabled")
        self.message_box.pack(pady=10)

        # Message entry box
        self.message_entry = tk.Entry(self.root, width=30)
        self.message_entry.pack(pady=5)

        # Send button
        send_button = tk.Button(self.root, text="Send Command", command=self.send_message)
        send_button.pack(pady=5)

        # Connect button
        connect_button = tk.Button(self.root, text="Connect to Server", command=self.connect_to_server)
        connect_button.pack(pady=5)

    def connect_to_server(self):
        if self.connected:
            messagebox.showinfo("Info", "Already connected to the server.")
            return
        
        try:
            # Connect to the server
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            messagebox.showinfo("Info", "Connected to the server.")
            
            # Start receiving messages in a separate thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def send_message(self):
        if not self.connected:
            messagebox.showerror("Error", "You need to connect to the server first.")
            return

        message = self.message_entry.get()
        if message:
            try:
                # Send message to server
                self.client_socket.send(message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send message: {e}")

    def receive_messages(self):
        while self.connected:
            try:
                # Receive messages from the server
                message = self.client_socket.recv(1024).decode('utf-8')

                if message:
                    self.display_message(message)
                else:
                    print("Server closed the connection")
                    self.connected = False
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        if not self.connected:
            self.disconnect()

    def display_message(self, message):
        # Update the message box with a new message
        self.message_box.config(state="normal")
        self.message_box.insert(tk.END, message + "\n")
        self.message_box.config(state="disabled")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False
        messagebox.showinfo("Info", "Disconnected from server.")

# Run the GUI application
root = tk.Tk()
app = InstructorClient(root)
root.mainloop()