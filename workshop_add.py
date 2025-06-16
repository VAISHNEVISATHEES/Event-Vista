import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def add_workshop_window(host_id):
    # Create a new window for adding workshop details
    add_window = tk.Toplevel()
    add_window.title("Add Workshop")

    # Make the window full-screen
    add_window.overrideredirect(True)
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()
    add_window.geometry(f"{screen_width}x{screen_height}+0+0")

    # Apply a ttk theme
    style = ttk.Style()
    style.theme_use('clam')

    # Set background color for the window
    add_window.configure(bg="#e8f0fe")

    # Customize ttk widgets
    style.configure("TLabel",
                    background="#e8f0fe",
                    font=("Arial", 14, "bold"),
                    foreground="#333")

    style.configure("TEntry",
                    padding=10,
                    font=("Arial", 12),
                    foreground="#333")

    style.configure("TButton",
                    padding=10,
                    relief="flat",
                    background="#1E3A8A",
                    foreground="white",
                    font=("Arial", 12, "bold"))

    style.map("TButton",
              background=[("active", "#274BDB")],
              foreground=[("active", "white")])

    # Create a container frame to center the content
    content_frame = tk.Frame(add_window, bg="#e8f0fe")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(content_frame, text="Add Workshop", font=("Arial", 20, "bold"), foreground="#1E3A8A").pack(pady=20)


    # Labels and entries for workshop details
    tk.Label(content_frame, text="Title:", bg="#e8f0fe", font=("Arial", 14, "bold"), fg="#333").pack(pady=(10, 5))
    title_entry = tk.Entry(content_frame, font=("Arial", 16), width=25)
    title_entry.pack(pady=5)

    tk.Label(content_frame, text="Description:", bg="#e8f0fe", font=("Arial", 14, "bold"), fg="#333").pack(pady=(10, 5))
    description_entry = tk.Entry(content_frame, font=("Arial", 16), width=25)
    description_entry.pack(pady=5)

    tk.Label(content_frame, text="Max Capacity:", bg="#e8f0fe", font=("Arial", 14, "bold"), fg="#333").pack(pady=(10, 5))
    capacity_entry = tk.Entry(content_frame, font=("Arial", 16), width=25)
    capacity_entry.pack(pady=5)

    tk.Label(content_frame, text="Cost:", bg="#e8f0fe", font=("Arial", 14, "bold"), fg="#333").pack(pady=(10, 5))
    cost_entry = tk.Entry(content_frame, font=("Arial", 16), width=25)
    cost_entry.pack(pady=5)

    tk.Label(content_frame, text="Date(Format:YYYY-MM-DD):", bg="#e8f0fe", font=("Arial", 14, "bold"), fg="#333").pack(pady=(10, 5))
    date_entry = tk.Entry(content_frame, font=("Arial", 16), width=25)
    date_entry.pack(pady=5)

    tk.Label(content_frame, text="Time:", bg="#e8f0fe", font=("Arial", 14, "bold"), fg="#333").pack(pady=(10, 5))
    time_entry = tk.Entry(content_frame, font=("Arial", 16), width=25)
    time_entry.pack(pady=5)

    def add_workshop():
        title = title_entry.get()
        description = description_entry.get()
        capacity = capacity_entry.get()
        cost = cost_entry.get()
        date = date_entry.get()
        time = time_entry.get()

        # Basic validation
        if not title or not description or not capacity or not cost or not date or not time:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Srivathsam123*",
                database="workshop_planner"
            )
            cursor = connection.cursor()

            # Insert the new workshop into the workshops table
            cursor.execute("INSERT INTO workshops (title, description, max_capacity, cost, date, time, host_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (title, description, int(capacity), float(cost), date, time, host_id))
            connection.commit()

            messagebox.showinfo("Success", "Workshop added successfully!")
            add_window.destroy()  # Close the add workshop window

            # Close connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

    # Button to add the workshop
    ttk.Button(content_frame, text="Add Workshop", command=add_workshop).pack(pady=20)

    # Button to close the window
    ttk.Button(content_frame, text="Close", command=add_window.destroy).pack(pady=10)

    add_window.mainloop()
