import streamlit as st
import google.generativeai as genai
from datetime import datetime
import re
from fpdf import FPDF

# Streamlit UI
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📝 AI Cover Letter Generator (Gemini)")

# API Key Input
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password")

# Form
with st.form("cover_letter_form"):
    full_name = st.text_input("Your Full Name")
    address = st.text_input("Your Address")
    phone = st.text_input("Your Phone Number")
    email = st.text_input("Your Email Address")
    job_title = st.text_input("Job Title You're Applying For")
    company_name = st.text_input("Company Name")
    skills = st.text_area("Your Skills and Experience")
    tone = st.selectbox("Tone of the Cover Letter", ["Professional", "Friendly", "Confident", "Formal", "Persuasive"])
    submitted = st.form_submit_button("Generate Cover Letter")

if submitted:
    if not api_key:
        st.error("❌ Please enter your Gemini API key.")
    else:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            today_date = datetime.today().strftime("%d %B %Y")

            # ✅ Build prompt (AI should NOT include personal details, we add manually)
            prompt = f"""
            Write a {tone.lower()} cover letter for applying to the position of {job_title} at {company_name}.
            The letter must:
            - Start with 'Dear Hiring Manager,'
            - NOT include my personal contact details (name, address, phone, email, date)
            - End with 'Sincerely, {full_name}'
            - Be concise, professional, and well-structured.
            
            Skills: {skills}
            """

            # Generate AI response
            with st.spinner("⏳ Generating your cover letter..."):
                response = model.generate_content([prompt])
                letter_body = re.sub(r"\[.*?\]", "", response.text).strip()

            # ✅ Create Header with proper indentation
            header = f"""{full_name}
{address}
Phone: {phone}
Email: {email}
Date: {today_date}

"""

            # ✅ Combine header and AI body
            final_letter = header + letter_body

            # ✅ Styled Output in Streamlit
            st.subheader("📄 Your Professionally Styled Cover Letter")
            st.markdown(f"""
            <div style='font-family: Arial; max-width:700px; line-height:1.6; font-size:16px; 
                        background:#fff; padding:20px; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1); 
                        white-space:pre-wrap;'>
                {final_letter}
            </div>
            """, unsafe_allow_html=True)

            # ✅ Generate PDF with the header at the top
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, final_letter)
            pdf_file = "cover_letter.pdf"
            pdf.output(pdf_file)

            # ✅ Download Buttons
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Cover Letter (PDF)", f, file_name="cover_letter.pdf", mime="application/pdf")
            st.download_button("📥 Download Cover Letter (TXT)", data=final_letter, file_name="cover_letter.txt")

        except Exception as e:
            st.error(f"❌ Error: {e}")
