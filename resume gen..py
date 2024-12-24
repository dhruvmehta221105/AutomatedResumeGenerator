import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
import webbrowser

class ResumeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Generator")
        self.root.geometry("700x900")
        self.root.configure(bg='#f7f7f7')
        self.root.resizable(False, False)

        # Title Label
        tk.Label(root, text="Resume Generator", font=("Arial", 24, "bold"), bg='#f7f7f7').pack(pady=20)

        # Input Fields
        self.name_var = tk.StringVar()
        self.father_name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.bio_var = tk.StringVar()
        self.education_var = tk.StringVar()
        self.experience_var = tk.StringVar()
        self.certificates_var = tk.StringVar()
        self.achievements_var = tk.StringVar()
        self.skills_var = tk.StringVar()
        self.image_path = None

        self.create_input_field("Name:", self.name_var)
        self.create_input_field("Father's Name:", self.father_name_var)
        self.create_input_field("Contact Number:", self.contact_var)
        self.create_input_field("Email:", self.email_var)
        self.create_input_field("Address:", self.address_var)
        self.create_input_field("Bio Data:", self.bio_var)
        self.create_input_field("Education Details:", self.education_var)
        self.create_input_field("Experience:", self.experience_var)
        self.create_input_field("Certificates:", self.certificates_var)
        self.create_input_field("Achievements:", self.achievements_var)
        self.create_input_field("Skills:", self.skills_var)

        # Image Upload
        tk.Button(root, text="Upload Image", command=self.upload_image, font=("Arial", 12), bg='#4CAF50', fg='white').pack(pady=10)
        self.image_label = tk.Label(root, bg='#f7f7f7')
        self.image_label.pack(pady=5)

        # Generate Resume Button
        tk.Button(root, text="Generate Resume", command=self.generate_resume_pdf, bg="green", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

    def create_input_field(self, label_text, variable):
        frame = tk.Frame(self.root, bg='#f7f7f7')
        frame.pack(anchor="w", padx=20, pady=10)
        tk.Label(frame, text=label_text, font=("Arial", 14), bg='#f7f7f7').pack(side="left")
        tk.Entry(frame, textvariable=variable, font=("Arial", 12), width=30).pack(side="left", padx=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.image_path = file_path
            img = Image.open(self.image_path)
            img.thumbnail((120, 120))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

    def generate_resume_pdf(self):
        # Get all input data
        name = self.name_var.get()
        father_name = self.father_name_var.get()
        contact = self.contact_var.get()
        email = self.email_var.get()
        address = self.address_var.get()
        bio = self.bio_var.get()
        education = self.education_var.get()
        experience = self.experience_var.get()
        certificates = self.certificates_var.get()
        achievements = self.achievements_var.get()
        skills = self.skills_var.get()

        if not all([name, father_name, contact, email, address, bio, education, experience, certificates, achievements, skills]):
            messagebox.showerror("Input Error", "Please fill all fields and upload an image.")
            return

        # Set PDF file path
        pdf_file_path = os.path.join(os.getcwd(), f"{name}_Resume.pdf")

        # Create PDF
        pdf = canvas.Canvas(pdf_file_path, pagesize=A4)
        width, height = A4

        # Set Title Fonts and Colors
        pdf.setFont("Helvetica-Bold", 20)
        y_position = height - 100
        section_gap = 50

        # Add Name and Image
        if self.image_path:
            img = Image.open(self.image_path)
            img.thumbnail((100, 100))
            img.save("temp_image.png")
            pdf.drawImage("temp_image.png", 50, y_position - 70, width=100, height=100)
            os.remove("temp_image.png")
            pdf.drawString(180, y_position, name)
        else:
            pdf.drawString(100, y_position, name)

        # Add details
        y_position -= section_gap
        self.add_pdf_field(pdf, "Father's Name:", father_name, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Contact Number:", contact, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Email:", email, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Address:", address, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Bio Data:", bio, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Education Details:", education, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Experience:", experience, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Certificates:", certificates, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Achievements:", achievements, y_position)

        y_position -= section_gap
        self.add_pdf_field(pdf, "Skills:", skills, y_position)

        # Save and Open PDF
        pdf