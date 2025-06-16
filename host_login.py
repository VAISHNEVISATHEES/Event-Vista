import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from workshop_add import add_workshop_window
from host_sign_up import host_sign_up_window
from fpdf import FPDF
import matplotlib.pyplot as plt

def generate_workshop_pdf(workshop_details, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add workshop details
    for key, value in workshop_details.items():
        if key != "Participants":  # Skip participants here
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")

    # Add participants table
    pdf.cell(200, 10, txt="", ln=True)  # Add some space
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Participants:", ln=True)
    pdf.set_font("Arial", size=12)

    if workshop_details["Participants"]:
        pdf.set_fill_color(169, 169, 169)  # grey background (RGB: 0, 0, 0)
        pdf.set_text_color(255, 255, 255)  # White text (RGB: 255, 255, 255)        
        pdf.cell(50, 10, txt="Name", border=1, align="C", fill=True)
        pdf.cell(50, 10, txt="Phone", border=1, align="C", fill=True)
        pdf.cell(50, 10, txt="Email", border=1, align="C", fill=True)
        pdf.cell(50, 10, txt="College", border=1, align="C", fill=True)
        pdf.ln()

        for participant in workshop_details["Participants"]:
            pdf.set_fill_color(255,255,255)
            pdf.set_text_color(0,0,0)
            pdf.cell(50, 10, txt=participant["name"], border=1, align="C", fill=True)
            pdf.cell(50, 10, txt=participant["phone"], border=1, align="C", fill=True)
            pdf.cell(50, 10, txt=participant["email"], border=1, align="C", fill=True)
            pdf.cell(50, 10, txt=participant["college"], border=1, align="C", fill=True)
            pdf.ln()
    else:
        pdf.cell(200, 10, txt="No participants registered.", ln=True, align="L")

    pdf.output(filename)

def generate_participant_graph(workshops):
    titles = [workshop[1] for workshop in workshops]
    participant_counts = [len(workshop[6]) for workshop in workshops]  # Use participant details length

    plt.figure(figsize=(10, 6))
    plt.bar(titles, participant_counts, color="skyblue")
    plt.xlabel("Workshops")
    plt.ylabel("Number of Participants")
    plt.title("Number of Participants per Workshop")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig("workshops_participant_graph.png")
    plt.show()
    print("Graph saved as 'workshops_participant_graph.png'")

def host_login_window():
    # Create a new login window
    login_window = tk.Toplevel()
    login_window.title("Host Login")
    login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}+0+0")
    login_window.configure(bg="#f0f4f8")  # Light gray-blue background

    # Set the window to full screen
    login_window.overrideredirect(True)  # Remove window decorations (title bar, borders, etc.)

    # Set the theme
    style = ttk.Style()
    style.theme_use("clam")  # Modern theme

    # Set background color for the window
    login_window.configure(bg="#e8f0fe")  # Light blue background

    # Add a title label
    content_frame = tk.Frame(login_window, bg="#e8f0fe")
    content_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    # Configure button style
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

    # Create the login window content
    ttk.Label(content_frame, text="Host Login", font=("Arial", 20, "bold"), foreground="#1E3A8A").pack(pady=20)

    # Labels and entries for username and password
    ttk.Label(content_frame, text="Username:").pack(pady=10, anchor="w")
    username_entry = ttk.Entry(content_frame, font=("Arial", 16), width=20)
    username_entry.pack(pady=10, anchor="w")

    ttk.Label(content_frame, text="Password:").pack(pady=10, anchor="w")
    password_entry = ttk.Entry(content_frame, show="*", font=("Arial", 16), width=20)
    password_entry.pack(pady=10, anchor="w")

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return

        try:
            # Connect to MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Srivathsam123*",  # Replace with your password
                database="workshop_planner"
            )
            cursor = connection.cursor()

            # Verify login credentials
            cursor.execute("SELECT id FROM hosts WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                host_id = result[0]
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                login_window.destroy()

                # Fetch all workshops created by the host
                cursor.execute(""" 
                    SELECT w.workshop_id, w.title, w.date, w.time, w.description, w.registrations
                    FROM workshops w
                    WHERE w.host_id = %s
                    GROUP BY w.workshop_id
                """, (host_id,))
                workshops = cursor.fetchall()

                # Include participant details
                for i, workshop in enumerate(workshops):
                    
                    workshop_id = workshop[0] 
                    cursor.execute(""" 
                        SELECT 
                            u.name AS user_name,
                            u.email AS user_email,
                            r.phone_number , r.college
                        FROM 
                            workshops w
                        JOIN 
                            registrations r ON w.workshop_id = r.workshop_id
                        JOIN 
                            users u ON r.user_id = u.user_id
                        WHERE 
                            w.host_id = %s AND w.workshop_id = %s
                    """, (host_id, workshop_id))
                    participants = cursor.fetchall()

                    workshops[i] = (*workshop, [{"name": p[0], "phone": p[1], "email": p[2], "college": p[3]} for p in participants])

                # Display workshops in a new window
                workshop_window = tk.Toplevel()
                workshop_window.title("Your Workshops")
                # Make the window full-screen
                workshop_window.overrideredirect(True)
                screen_width = workshop_window.winfo_screenwidth()
                screen_height = workshop_window.winfo_screenheight()
                workshop_window.geometry(f"{screen_width}x{screen_height}+0+0")

                # Apply a ttk theme
                style = ttk.Style()
                style.theme_use('clam')

                # Set background color for the window
                workshop_window.configure(bg="#e8f0fe")

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
                        background=[["active", "#274BDB"]],
                        foreground=[["active", "white"]])

                if not workshops:
                    ttk.Label(workshop_window, text="No workshops created yet.", font=("Arial", 14)).pack(pady=20)
                else:
                    ttk.Label(workshop_window, text="Workshops and Participants", font=("Arial", 16,"bold")).pack(pady=10)

                    frame = tk.Frame(workshop_window, bg="#e8f0fe")
                    frame.pack(pady=10, fill="both", expand=True)

                    for index, workshop in enumerate(workshops):
                        workshop_id, title, date, time, description, registrations, participants = workshop

                        # Create a frame for each card
                        card = tk.Frame(frame, bg="#ffffff", bd=1, relief="solid",width=350, height=400)
                        card.grid(row=index // 5, column=index % 5, padx=20, pady=20, sticky="nsew")

                        # Populate the card with details
                        tk.Label(card, text=f"Title: {title}", font=("Arial", 16, "bold"), bg="#ffffff", anchor="w").pack(anchor="w")
                        tk.Label(card, text=f"Date: {date}", font=("Arial", 14), bg="#ffffff", anchor="w").pack(anchor="w")
                        tk.Label(card, text=f"Time: {time}", font=("Arial", 14), bg="#ffffff", anchor="w").pack(anchor="w")
                        tk.Label(card, text=f"Description: {description}", font=("Arial", 14), bg="#ffffff", anchor="w", wraplength=150).pack(anchor="w")
                        tk.Label(card, text=f"No.of.Registertaions: {registrations}", font=("Arial", 14), bg="#ffffff", anchor="w").pack(anchor="w")
            

                    # Button to generate PDFs
                    def generate_all_pdfs():
                        for workshop in workshops:
                            workshop_id, title, date, time, description, registrations, participants = workshop
                            workshop_details = {
                                "Title": title,
                                "Date": date,
                                "Time": time,
                                "Description": description,
                                "Registration": registrations,
                                "Participants": participants
                            }
                            filename = f"{title.replace(' ', '_')}_details.pdf"
                            generate_workshop_pdf(workshop_details, filename)
                            print(f"PDF Generated: {filename}")
                        messagebox.showinfo("PDFs Generated", "PDFs for all workshops have been created successfully.")

                    ttk.Button(workshop_window, text="Generate PDFs", command=generate_all_pdfs).pack(pady=10)

                    # Button to generate graph
                    def generate_graph():
                        generate_participant_graph(workshops)
                        messagebox.showinfo("Graph Generated", "Graph for participant counts has been generated and saved.")

                    ttk.Button(workshop_window, text="Generate Graph", command=generate_graph).pack(pady=10)

                # Add Workshop Button
                ttk.Button(workshop_window, text="Add Workshop", command=lambda: add_workshop_window(host_id)).pack(pady=10)
                ttk.Button(workshop_window, text="Close", command=workshop_window.destroy).pack(pady=10)

            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")

    ttk.Button(content_frame, text="Login", command=verify_login, width=10).pack(pady=20)

    ttk.Label(content_frame, text="Don't have an account?").pack(pady=5)
    ttk.Button(content_frame, text="Sign Up", command=host_sign_up_window, width=10).pack(pady=5)

    # Add a close button for convenience (Optional: smaller than login button)
    close_button = ttk.Button(content_frame, text="Close", command=login_window.destroy, width=10)
    close_button.pack(pady=10)

    login_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Host Login")
    ttk.Button(root, text="Host Login", command=host_login_window).pack(pady=20)
    root.mainloop()
