
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

def generate_workshop_pdf(workshop_details, output_path):
   
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Workshop Details", ln=True, align='C')
    pdf.ln(10)  # Add a line break

    for key, value in workshop_details.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')



    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")

def generate_participant_chart(data, output_path):
   
    workshops = list(data.keys())
    participants = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(workshops, participants, color='skyblue')
    plt.xlabel('Workshops')
    plt.ylabel('Number of Participants')
    plt.title('Workshop Participation')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    print(f"Chart saved successfully: {output_path}")

# Example usage
if __name__ == "__main__":
    # Example workshop details
    workshop_details = {
        "Title": "Python Basics",
        "Date": "2024-12-30",
        "Time": "10:00 AM - 1:00 PM",
        "Description": "An introductory workshop on Python programming."
    }

    # Generate PDF
    pdf_output_path = "workshop_details.pdf"
    generate_workshop_pdf(workshop_details, pdf_output_path)

    # Example participant data
    participant_data = {
        "Python Basics": 25,
        "Data Science 101": 30,
        "Web Development": 20
    }

    # Generate chart
    chart_output_path = "participant_chart.png"
    generate_participant_chart(participant_data, chart_output_path)
