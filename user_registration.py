import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Function to handle user registration
def user_sign_up_window():
    # Create the sign-up window
    sign_up_window = tk.Toplevel()
    sign_up_window.title("User Registration")

    # Remove window decorations (title bar, borders, etc.)
    sign_up_window.overrideredirect(True)

    # Get screen dimensions
    screen_width = sign_up_window.winfo_screenwidth()
    screen_height = sign_up_window.winfo_screenheight()

    # Set the window size to full screen
    sign_up_window.geometry(f"{screen_width}x{screen_height}+0+0")  # Fullscreen at (0,0)

    # Set the theme to 'clam'
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' or another modern ttk theme

    # Set background color for the window
    sign_up_window.configure(bg="#e8f0fe")  # Light blue background for the window

    # Customize ttk widgets
    style.configure("TLabel",
                    background="#e8f0fe",  # Label background matches window
                    font=("Arial", 14, "bold"),
                    foreground="#333")  # Dark gray text color

    style.configure("TEntry",
                    padding=10,
                    font=("Arial", 12),
                    foreground="#333")

    style.configure("TButton",
                    padding=10,
                    relief="flat",
                    background="#1E3A8A",  # Dark blue background
                    foreground="white",
                    font=("Arial", 12, "bold"))

    # Add hover effects to buttons
    style.map("TButton",
              background=[("active", "#274BDB")],  # Slightly lighter blue on hover
              foreground=[("active", "white")])

    # Create a container frame to center the content
    content_frame = tk.Frame(sign_up_window, bg="#e8f0fe")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add a title label
    ttk.Label(content_frame, text="User Registration", font=("Arial", 20, "bold"), foreground="#1E3A8A").pack(pady=20)

    # Center-align the labels and entries using `pack` with additional spacing
    ttk.Label(content_frame, text="Username:").pack(pady=(10, 5))
    username_entry = ttk.Entry(content_frame, font=("Arial", 16), width=20)
    username_entry.pack(pady=5)

    ttk.Label(content_frame, text="Email:").pack(pady=10)
    email_entry = ttk.Entry(content_frame, font=("Arial", 16), width=20)
    email_entry.pack(pady=5)

    ttk.Label(content_frame, text="Password:").pack(pady=10)
    password_entry = ttk.Entry(content_frame, show="*", font=("Arial", 16), width=20)
    password_entry.pack(pady=5)

    # Function to create account
    def create_account():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        # Basic validation
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if '@' not in email:
            messagebox.showerror("Error","Please enter a valid email address")
            return

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",  # Adjust if needed
                user="root",       # MySQL username
                password="Srivathsam123*",  # MySQL password
                database="workshop_planner"  # Your database name
            )
            cursor = connection.cursor()

            # Check if the username or email already exists
            cursor.execute("SELECT * FROM users WHERE name = %s OR email = %s", (username, email))
            result = cursor.fetchone()

            if result:
                messagebox.showerror("Error", "Username or Email already exists!")
            else:
                # Insert new user into the users table
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (username, email, password))
                connection.commit()
                messagebox.showinfo("Success", "User account created successfully!")
                sign_up_window.destroy()  # Close the sign-up window

            # Close connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

    # Button to create a new user account
    ttk.Button(content_frame, text="Create Account", command=create_account).pack(pady=20)

    # Add a button to close the full-screen window
    ttk.Button(content_frame, text="Close", command=sign_up_window.destroy).pack(pady=10)

    # Run the sign-up window
    sign_up_window.mainloop()

# Sample function call to create a sign-up window
# user_sign_up_window()
