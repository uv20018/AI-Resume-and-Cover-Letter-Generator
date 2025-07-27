import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
import textwrap
import unicodedata  # ✅ To clean Unicode characters

# 🔐 DIRECTLY set your Gemini API Key here (not recommended for production)
genai.configure(api_key="AIzaSyBN0KhNhjqBLED3vi8PJzKgiAGNdww1Y8o")

# 🔧 Function to clean Unicode characters
def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

# 📄 Export resume text to PDF (safe, no .ttf needed)
def export_to_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    cleaned_text = clean_text(text)

    for line in cleaned_text.split('\n'):
        line = line.strip()
        if not line:
            pdf.ln(5)  # Blank line spacing
            continue

        wrapped = textwrap.wrap(line, width=90)
        for wline in wrapped:
            pdf.cell(0, 10, txt=wline, ln=True)

    pdf.output(filename)

# 🧠 Generate resume using Gemini
def generate_resume(name, email, phone, education, skills, experience, career_goal):
    prompt = f"""
    Create a professional resume in plain text format using the following user information:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Education: {education}
    Skills: {skills}
    Work Experience: {experience}
    Career Objective: {career_goal}

    Include clear sections: Summary, Skills, Education, Experience, and Objective.
    """

    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

# 🌐 Streamlit UI
st.title("🧠 AI Resume Generator (Gemini)")
st.markdown("Enter your details to generate a resume using Google's Gemini AI.")

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
education = st.text_area("Education Background")
skills = st.text_area("Skills (comma-separated)")
experience = st.text_area("Work Experience")
career_goal = st.text_area("Career Objective")

if st.button("Generate Resume"):
    if all([name, email, phone, education, skills, experience, career_goal]):
        with st.spinner("Generating your resume with Gemini..."):
            resume_text = generate_resume(name, email, phone, education, skills, experience, career_goal)
            st.success("✅ Resume generated successfully!")

            st.subheader("📝 Your AI-Generated Resume:")
            st.text(resume_text)

            # Save and offer PDF download
            filename = "resume.pdf"
            export_to_pdf(resume_text, filename)

            with open(filename, "rb") as pdf_file:
                st.download_button("📄 Download Resume PDF", pdf_file, file_name=filename, mime="application/pdf")

            os.remove(filename)
    else:
        st.warning("⚠️ Please fill all fields to generate the resume.")
