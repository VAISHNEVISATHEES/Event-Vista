import tkinter as tk
from tkinter import messagebox
import mysql.connector

def collect_user_details_and_register(user_id, workshop_id):
    # Create a user details form
    details_window = tk.Toplevel()
    details_window.title("Enter Your Details")
    details_window.geometry("400x350")

    # Labels and input fields
    tk.Label(details_window, text="Enter Your Details", font=("Arial", 16)).pack(pady=10)

    tk.Label(details_window, text="Name:").pack(anchor="w", padx=10)
    name_entry = tk.Entry(details_window)
    name_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(details_window, text="College:").pack(anchor="w", padx=10)
    college_entry = tk.Entry(details_window)
    college_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(details_window, text="Email:").pack(anchor="w", padx=10)
    email_entry = tk.Entry(details_window)
    email_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(details_window, text="Phone Number:").pack(anchor="w", padx=10)
    phone_entry = tk.Entry(details_window)
    phone_entry.pack(fill="x", padx=10, pady=5)

    def submit_details():
        name = name_entry.get()
        college = college_entry.get()
        email = email_entry.get()
        phone_number = phone_entry.get()

        # Validate inputs
        if not name or not college or not email or not phone_number:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Simple validation for email and phone number
        if '@' not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if len(phone_number) != 10 or not phone_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
            return

        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Srivathsam123*",  # Replace with your password
                database="workshop_planner"
            )
            cursor = connection.cursor()

            # Insert user details into the registrations table
            cursor.execute(
                """
                INSERT INTO registrations (user_id, workshop_id, name, college, email, phone_number) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (user_id, workshop_id, name, college, email, phone_number)
            )
            connection.commit()

            # Increment the registration count
            cursor.execute(
                "UPDATE workshops SET registrations = registrations + 1 WHERE workshop_id = %s",
                (workshop_id,)
            )
            connection.commit()

            messagebox.showinfo("Success", "You have successfully registered for the workshop!")
            cursor.close()
            connection.close()
            details_window.destroy()  # Close the user details form

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    # Submit button
    tk.Button(details_window, text="Submit", command=submit_details).pack(pady=10) 