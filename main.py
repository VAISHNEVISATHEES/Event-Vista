import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mysql.connector
from user_login import user_login_window
from host_login import host_login_window
from user_registration import user_sign_up_window

# Database connection function
def create_connection():
    """Establish and return a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Srivathsam123*",
            database="workshop_planner"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None

# User registration function
def user_registration():
    user_sign_up_window()

# Host login function
def host_login():
    host_login_window()

# User login function
def user_login():
    user_login_window()

# Function to update the video background
def update_video():
    """Read and display video frames on the tkinter canvas."""
    ret, frame = video_capture.read()
    if ret:
        # Resize frame to match the screen size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        frame = cv2.resize(frame, (screen_width, screen_height))

        # Convert frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

        # Update the label with the video frame
        video_label.config(image=frame_image)
        video_label.image = frame_image

    # Schedule the next frame update
    root.after(15, update_video)

# Main tkinter GUI with full-screen video background
def main_window():
    global root, video_label, video_capture

    # Initialize tkinter window
    root = tk.Tk()
    root.title("EventVista")

    # Make the window full-screen
    root.attributes("-fullscreen", True)

    # Create video capture object
    video_capture = cv2.VideoCapture("workshop.mov")  # Replace with your video file path

    # Add a label for video playback
    video_label = tk.Label(root)
    video_label.pack(fill=tk.BOTH, expand=True)

    # Add a label for displaying "EventVista" text
    title_label = tk.Label(root, text="EventVista", font=("Arial", 36, "bold"), fg="black", bg="white")
    title_label.place(relx=0.5, rely=0.1, anchor="center")  # Position at the top center


    # Create a frame for buttons without background
    button_frame = tk.Frame(root)  # No background for the frame
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Button styling options (using labels)
    button_style = {
        "fg": "#000000",  # Black text
        "font": ("Arial", 18, "bold"),  # Increased font size for better visibility
        "relief": tk.FLAT,  # Flat design (no borders)
        "bd": 0,  # No border
        "bg": None,  # No background for label (making it transparent)
        "highlightthickness": 0,  # No highlight border
        "activebackground": None,  # No background change on click
        "activeforeground": "#000000",  # Text color when clicked
    }

    # Create labels that behave like buttons
    def create_transparent_button(text, command):
        label = tk.Label(button_frame, text=text, **button_style, width=30, height=2)  # Increase width for a wider button
        label.pack(padx=20, pady=20)  # Added padding for space inside the button
        label.bind("<Button-1>", lambda event: command())  # Simulate button click
        return label

    create_transparent_button("User Registration", user_registration)
    create_transparent_button("Host Login", host_login)
    create_transparent_button("User Login", user_login)

    # Start video playback
    update_video()

    # Bind escape key to exit full-screen
    root.bind("<Escape>", lambda e: root.destroy())

    # Start the tkinter main loop
    root.mainloop()

    # Release video capture object
    video_capture.release()

# Program Entry Point
if __name__ == "__main__":
    # Test database connection
    db_connection = create_connection()
    if db_connection:
        db_connection.close()

    # Launch the main application window
    main_window()
