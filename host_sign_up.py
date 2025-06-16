#host_sign_up.py
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def host_sign_up_window():
    # Create a new sign-up window
    sign_up_window = tk.Toplevel()
    sign_up_window.title("Host Sign Up")
    sign_up_window.geometry("400x300")
    sign_up_window.geometry(f"{sign_up_window.winfo_screenwidth()}x{sign_up_window.winfo_screenheight()}+0+0")
    sign_up_window.configure(bg="#f0f4f8")  # Light gray-blue background

    # Set the window to full screen
    sign_up_window.overrideredirect(True)  # Remove window decorations 

    # Set the theme
    style = ttk.Style()
    style.theme_use("clam")  
    
    # Set background color for the window
    sign_up_window.configure(bg="#e8f0fe")  # Light blue background

    # Add a title label
    content_frame = tk.Frame(sign_up_window, bg="#e8f0fe")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Configure button style
    # Configure ttk widget styles
    style.configure("TLabel",
                    background="#e8f0fe",  # Label background matches window
                    font=("Arial", 14, "bold"),
                    foreground="#333")  # Dark gray text color

    style.configure("TEntry",
                    padding=10,
                    font=("Arial", 16),  # Increased font size for better readability
                    foreground="#333",
                    width=40)  # Increased width for better visibility

    style.configure("TButton",
                    padding=10,
                    relief="flat",
                    background="#1E3A8A",  # Dark blue button background
                    foreground="white",
                    font=("Arial", 14, "bold"),
                    width=20)  # Adjusted width for buttons
    
    # Create a container frame to center the content
    content_frame = tk.Frame(sign_up_window, bg="#e8f0fe")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    ttk.Label(content_frame, text="Host Signup", font=("Arial", 20, "bold"), foreground="#1E3A8A").pack(pady=20)

    # Labels and entries for username and password
    ttk.Label(content_frame, text="Username:").pack(pady=10, anchor="w")
    username_entry = ttk.Entry(content_frame, font=("Arial", 16), width=20)
    username_entry.pack(pady=10, anchor="w")

    ttk.Label(content_frame, text="Password:").pack(pady=10, anchor="w")
    password_entry = ttk.Entry(content_frame, show="*", font=("Arial", 16), width=20)
    password_entry.pack(pady=10, anchor="w")

    def create_account():
        username = username_entry.get()
        password = password_entry.get()

        # Basic validation
        if not username or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Srivathsam123*",  # Your MySQL password
                database="workshop_planner"  # Your database name
            )
            cursor = connection.cursor()

            # Check if the username already exists
            cursor.execute("SELECT * FROM hosts WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                messagebox.showerror("Error", "Username already exists!")
            else:
                # Insert new host into the hosts table
                cursor.execute("INSERT INTO hosts (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                messagebox.showinfo("Success", "Host account created successfully!")
                sign_up_window.destroy()  # Close the sign-up window

            # Close connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

    # Create Account button
    signup_button = ttk.Button(content_frame, text="Create Account", command=create_account, width=20)
    signup_button.pack(pady=10)

    # Close button
    close_button = ttk.Button(content_frame, text="Close", command=sign_up_window.destroy, width=20)
    close_button.pack(pady=10)

    sign_up_window.mainloop()
