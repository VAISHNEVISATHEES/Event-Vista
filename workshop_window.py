import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def display_workshops(user_id):
    # Create a new window to display workshops
    workshop_window = tk.Toplevel()
    workshop_window.title("Available Workshops")
    
    # Set the window to fullscreen with theme
    workshop_window.geometry(f"{workshop_window.winfo_screenwidth()}x{workshop_window.winfo_screenheight()}+0+0")
    workshop_window.configure(bg="#f0f4f8")  # Light gray-blue background
    
    # Set the theme
    style = ttk.Style()
    style.theme_use("clam")  # Modern theme

    # Set background color for the window
    workshop_window.configure(bg="#e8f0fe")  # Light blue background

    # Create a Frame to hold the content side-by-side
    main_frame = tk.Frame(workshop_window, bg="#e8f0fe")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Create a canvas and scrollable region to hold the workshops
    canvas = tk.Canvas(main_frame, bg="#e8f0fe")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind_all("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    workshop_frame = tk.Frame(canvas, bg="#e8f0fe")
    canvas.create_window((0, 0), window=workshop_frame, anchor="nw")

    try:
        # Connect to MySQL database to fetch workshops
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Srivathsam123*",  # Replace with your password
            database="workshop_planner"
        )
        cursor = connection.cursor()

        # Fetch all workshops
        cursor.execute("SELECT * FROM workshops")
        workshops = cursor.fetchall()

        # Set the number of columns for the grid layout (5 cards in a row)
        columns = 5  # Change to 5 columns
        row = 0

        # Configure grid to ensure equal column width
        for col in range(columns):
            workshop_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        for i, workshop in enumerate(workshops):
            workshop_id = workshop[0]
            title = workshop[1]
            description = workshop[2]
            max_capacity = workshop[3]
            registrations = workshop[4]
            cost = workshop[5]
            date = workshop[6]
            time = workshop[8]

            # Create a frame for each workshop to display it like a card
            workshop_card = tk.Frame(workshop_frame, bg="#ffffff", relief="solid", bd=1, width=350, height=300)
            workshop_card.grid(row=row, column=i % columns, padx=10, pady=10, sticky="nsew")

            # Add content to the card
            tk.Label(workshop_card, text=title, font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
            tk.Label(workshop_card, text=f"Description: {description}", bg="#ffffff", wraplength=300).pack(pady=5)
            tk.Label(workshop_card, text=f"Max Capacity: {max_capacity}", bg="#ffffff").pack(pady=5)
            tk.Label(workshop_card, text=f"Registrations: {registrations}", bg="#ffffff").pack(pady=5)
            tk.Label(workshop_card, text=f"Cost: {cost}", bg="#ffffff").pack(pady=5)
            tk.Label(workshop_card, text=f"Date: {date}", bg="#ffffff").pack(pady=5)
            tk.Label(workshop_card, text=f"Time: {time}", bg="#ffffff").pack(pady=5)

            # Function to open user details form
            def open_user_details_form(workshop_id, registrations, user_id, max_capacity):
                # Open a new window to collect user details
                details_window = tk.Toplevel()
                details_window.title("Enter Your Details")
                details_window.geometry("400x300")

                # Add input fields for user details
                tk.Label(details_window, text="Enter Your Details", font=("Arial", 16)).pack(pady=10)
                tk.Label(details_window, text="Name:").pack(anchor="w", padx=10)
                name_entry = tk.Entry(details_window)
                name_entry.pack(fill="x", padx=10, pady=5)

                tk.Label(details_window, text="Email:").pack(anchor="w", padx=10)
                email_entry = tk.Entry(details_window)
                email_entry.pack(fill="x", padx=10, pady=5)

                tk.Label(details_window, text="Phone:").pack(anchor="w", padx=10)
                phone_entry = tk.Entry(details_window)
                phone_entry.pack(fill="x", padx=10, pady=5)

                tk.Label(details_window, text="College:").pack(anchor="w", padx=10)
                college_entry = tk.Entry(details_window)
                college_entry.pack(fill="x", padx=10, pady=5)

                # Function to save user details and register for the workshop
                def submit_user_details():
                    name = name_entry.get()
                    email = email_entry.get()
                    phone = phone_entry.get()
                    college = college_entry.get()

                    # Validate the inputs
                    if not name or not email or not phone or not college:
                        messagebox.showerror("Error", "All fields are required!")
                        return

                    try:
                        # Register the user for the workshop
                        if registrations >= max_capacity:
                            messagebox.showwarning("Full", "This workshop is full!")
                        else:
                            # Insert the user_id and user details into the registration table
                            cursor.execute(
                                """
                                INSERT INTO registrations (user_id, workshop_id, name, email, phone_number, college)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """,
                                (user_id, workshop_id, name, email, phone, college)
                            )
                            connection.commit()

                            # Update registrations in the workshops table
                            cursor.execute(
                                "UPDATE workshops SET registrations = registrations + 1 WHERE workshop_id = %s",
                                (workshop_id,)
                            )
                            connection.commit()

                            messagebox.showinfo("Success", "Successfully registered for the workshop!")
                            details_window.destroy()  # Close the details window
                            workshop_window.destroy()  # Close the workshop window
                    except mysql.connector.Error as e:
                        messagebox.showerror("Error", f"Error registering for workshop: {e}")

                # Add a submit button to the user details form
                tk.Button(details_window, text="Submit", command=submit_user_details).pack(pady=10)

            # Updated button to open user details form
            tk.Button(
                workshop_card,
                text="Register",
                command=lambda w_id=workshop_id, reg=registrations: open_user_details_form(w_id, reg, user_id, max_capacity)
            ).pack(pady=10)

            # Update the row position when the column is full
            if i % columns == columns - 1:
                row += 1

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")

    finally:
        # Ensure proper cleanup of database connection and cursor
        try:
            if 'cursor' in locals() and cursor.is_connected():
                cursor.close()
            if 'connection' in locals() and connection.is_connected():
                connection.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Cleanup Error", f"Error during cleanup: {e}")

    workshop_window.mainloop()
