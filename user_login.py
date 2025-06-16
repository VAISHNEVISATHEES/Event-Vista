import tkinter as tk  # For basic tkinter GUI components
from tkinter import messagebox  # For pop-up messages (error, info)
from tkinter import ttk  # For themed widgets like buttons, labels, etc.
import mysql.connector  # To connect to MySQL and verify credentials
from workshop_window import display_workshops  # To call the display_workshops function after successful login


# Function to handle user login
def user_login_window():
    # Create the login window
    login_window = tk.Toplevel()
    login_window.title("User Login")

    # Set the window to full screen
    login_window.overrideredirect(True)  # Remove window decorations (title bar, borders, etc.)
    login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}+0+0")

    # Set the theme
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern ttk theme like 'clam'

    # Set background color for the window
    login_window.configure(bg="#e8f0fe")  # Light blue background

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
                    width=20)  # Adjusted width for Login button

    # Create a container frame to center the content
    content_frame = tk.Frame(login_window, bg="#e8f0fe")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Add a title label
    ttk.Label(content_frame, text="User Login", font=("Arial", 20, "bold"), foreground="#1E3A8A").pack(pady=20)

    # Center-align labels and entries using `pack`
    ttk.Label(content_frame, text="Email:").pack(pady=10)
    email_entry = ttk.Entry(content_frame, font=("Arial", 16), width=20)  # Set larger font size and width for email entry
    email_entry.pack(pady=10)

    ttk.Label(content_frame, text="Password:").pack(pady=10)
    password_entry = ttk.Entry(content_frame, font=("Arial", 16), show="*", width=20)  # Set larger font size and width for password entry
    password_entry.pack(pady=10)

    # Function to verify login
    def verify_login():
        email = email_entry.get()
        password = password_entry.get()

        # Check if both fields are filled
        if not email or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return

        # For debugging, print and show the entered email and password (never do this in production)
        print(f"Entered Email: {email}")
        print(f"Entered Password: {password}")
        messagebox.showinfo("Entered Data", f"Email: {email}\nPassword: {password}")  # Remove this in production

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Srivathsam123*",  # Replace with your MySQL password
                database="workshop_planner"  # Your database name
            )
            cursor = connection.cursor()

            # Check if the user exists with the given email and password
            cursor.execute("SELECT user_id, name FROM users WHERE email = %s AND password = %s", (email, password))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                messagebox.showinfo("Login Successful", f"Welcome, {result[1]}!")  # result[1] is the username
                login_window.destroy()  # Close the login window
                display_workshops(user_id)  # Open the workshops screen
            else:
                messagebox.showerror("Login Failed", "Invalid email or password")

            # Close connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

    # Button to verify login
    login_button = ttk.Button(content_frame, text="Login", command=verify_login, width=10)
    login_button.pack(pady=20)

    # Add a close button for convenience (Optional: smaller than login button)
    close_button = ttk.Button(content_frame, text="Close", command=login_window.destroy, width=10)
    close_button.pack(pady=10)

    # Run the login window
    login_window.mainloop()
