import tkinter as tk
from tkinter import messagebox
import socket
import threading
import cv2
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer 

# Server configuration
SERVER_HOST = '129.8.203.100'
SERVER_PORT = 5000

class InstructorClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Instructor Client")
        self.root.geometry("900x700")
        
        # Video playback state
        self.video_running = False
        self.video_capture = None
        self.media_player = None

        # Connection status
        self.connected = False
        self.client_socket = None

        #username
        self.username = None
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()


# ------------------------------------- GUI components ----------------------------------------------------------------------
        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(self.root, text="Instructor Client", font=("Arial", 16))
        title_label.pack(pady=10)

        # Room canvas for video playback
        self.room_canvas = tk.Canvas(self.root, width=800, height=500)
        self.room_canvas.pack()


          # Video playback screen in the room
        self.video_label = tk.Label(self.room_canvas)
        self.room_canvas.create_window(400, 250, window=self.video_label, width=640, height=360)

        # Controls
        play_button = tk.Button(self.root, text="Play Video", command=self.play_video)
        play_button.pack(side="left", padx=50, pady=10)

        stop_button = tk.Button(self.root, text="Stop Video", command=self.stop_video)
        stop_button.pack(side="left", padx=25, pady=10)

    
        connect_button = tk.Button(self.root, text="Connect to Server", command=self.connect_to_server)
        connect_button.pack(side="right", padx=50, pady=10)

        disconnect_button = tk.Button(self.root, text="Disconnect", command=self.disconnect)
        disconnect_button.pack(side="right", padx=25, pady=10)

          #Chat box
        self.message_box = tk.Text(self.root, height=8, width=80, state="disabled")
        self.message_box.pack(padx =10, pady=10)

        # Message entry box
        self.message_entry = tk.Entry(self.root, width=100)
        self.message_entry.pack(padx=10, pady=10)

        #Send button
        send_button = tk.Button(self.root, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=10)

        self.assign_button = tk.Button(self.root, text="Assign Student", command=self.assign_student_to_room)
        self.assign_button.pack(pady=5)


# -------------------------------------- Socket methods ----------------------------------------------------------------------
    def connect_to_server(self):
        if self.connected:
            messagebox.showinfo("Info", "Already connected to the server.")
            return
        
        try:
            # Connect to the server
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            #set username attribute
            self.username = self.username_entry.get()
            #send username to server
            self.client_socket.send(self.username.encode('utf-8'))
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
                # format the message as <username>: <message>
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
                print(f"Received message: {message}") #debug print
                if message:
                    self.display_message(message)
                else:
                    print("Server closed the connection")
                    self.connected = False
                    break
            except Exception as e:
                messagebox.showerror("Error", f"Error receiving message: {e}")
                messagebox.showerror("Error", f"Failed to receive message: {e}")
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

    def assign_student_to_room(self):
        if not self.connected:
            messagebox.showerror("Error", "You need to connect to the server first.")
            return

        student = self.student_entry.get()
        room = self.room_entry.get()
        if student and room:
            try:
                command = f"/assign {student} {room}"
                self.client_socket.send(command.encode('utf-8'))
                self.display_message(f"Assigned {student} to {room}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to assign student: {e}")



 # -------------------------- VIDEO COMPONENTS -------------------------------------------------------
    def play_video(self):
        video_path = 'videos/video1.mp4'
        self.video_capture = cv2.VideoCapture(video_path)
        self.media_player = MediaPlayer(video_path)
        self.video_running = True
        self.update_frame()


        """   if not self.video_running:
            self.video_running = True
            video_thread = threading.Thread(target=self.show_video, args=("videos/video1.mp4",))
            video_thread.start()
        """
    def stop_video(self):
        self.video_running = False
        if self.video_capture:
            self.video_capture.release()
        if self.media_player:
            self.media_player.close()
            self.video_capture = None
        
    def pause_video(self):
        self.video_running = True


    def show_video(self, video_path):
        self.video_capture = cv2.VideoCapture(video_path)

        while self.video_running and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.root.after(0,self.update_image,imgtk) # attempt to fix flicker in image and error when quitting program regaring image
            cv2.waitKey(30)
        #self.video_capture.release()

    def update_frame(self):
           if self.video_running:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
                audio_frame, val = self.media_player.get_frame()
                if val != 'eof' and audio_frame is not None:
                    img, t = audio_frame
                self.root.after(10, self.update_frame)
            else:
                self.stop_video()
   

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = InstructorClient(root)
    root.mainloop()