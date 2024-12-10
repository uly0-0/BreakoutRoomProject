import tkinter as tk
from tkinter import messagebox
import socket
import threading
import cv2
from PIL import Image, ImageTk


# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000


class MovieTheaterClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Movie Theater Client")
        self.root.geometry("800x600")  # Adjusted for larger room

        # Video playback state
        self.video_running = False
        self.video_capture = None

        # Connection status
        self.connected = False
        self.client_socket = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(self.root, text="Virtual Movie Theater", font=("Arial", 16))
        title_label.pack(pady=10)

        # Video playback screen in the room
        self.video_label = tk.Label(self.room_canvas)
        self.room_canvas.create_window(400, 250, window=self.video_label, width=640, height=360)

        # Controls
        play_button = tk.Button(self.root, text="Play Video", command=self.play_video)
        play_button.pack(side="left", padx=10, pady=10)

        stop_button = tk.Button(self.root, text="Stop Video", command=self.stop_video)
        stop_button.pack(side="left", padx=10, pady=10)

        connect_button = tk.Button(self.root, text="Connect to Server", command=self.connect_to_server)
        connect_button.pack(side="left", padx=10, pady=10)

        disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect)
        disconnect_button.pack(side="left", padx=10, pady=10)

    def play_video(self):
        if not self.video_running:
            self.video_running = True
            video_thread = threading.Thread(target=self.show_video, args=("video/videoplayback.mp4",))
            video_thread.start()

    def stop_video(self):
        self.video_running = False
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None

    def show_video(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)

        while self.video_running and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.video_label.update()

        self.stop_video()

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

            # Start receiving messages
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
                    print(f"Server: {message}")
                else:
                    self.connected = False
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False
        messagebox.showinfo("Info", "Disconnected from server.")


# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieTheaterClient(root)
    root.mainloop()
