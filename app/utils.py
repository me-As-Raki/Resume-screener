import PyPDF2
import re
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import openai

# Load .env for sensitive credentials
load_dotenv()

# ----------------- TEXT EXTRACTION FROM PDF -----------------
def extract_text_from_pdf(file):
    """
    Extracts and returns lowercase text from a PDF file.
    """
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + " "
    return text.lower()

# ----------------- TEXT TOKENIZER -----------------
def tokenize(text):
    """
    Tokenize input text into lowercase words, removing punctuation.
    """
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

# ----------------- RESUME MATCH ANALYSIS -----------------
def analyze_resume(resume_text, jd_text):
    """
    Analyze resume vs. job description:
    - matched skills
    - missing skills
    - match score (%)
    """
    resume_words = set(tokenize(resume_text))
    jd_words = set(tokenize(jd_text))

    matched = sorted(resume_words & jd_words)
    missing = sorted(jd_words - resume_words)

    score = int((len(matched) / len(jd_words)) * 100) if jd_words else 0

    return {
        'matched': matched,
        'missing': missing,
        'score': score
    }

# ----------------- SEND EMAIL TO CANDIDATE -----------------
def send_email(to_email, subject, body):
    """
    Sends an email via Gmail SMTP.
    Credentials are loaded from environment variables.
    """
    try:
        EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")       # e.g. rakeshpoojary850@gmail.com
        EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")   # Your app password from .env

        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            raise ValueError("Email credentials not set in .env")

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load the Gemini API key from environment variable
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_ai_suggestions(resume_text, jd_text):
    try:
        prompt = f"""
You are a professional resume advisor.

Your task is to review the resume and job description provided below. Then, suggest exactly 5 to 6 concise and actionable improvements to the resume.

Focus areas:
- Identify missing or weak skills (especially technical ones like React, Python, APIs, etc.)
- Recommend ways to quantify achievements (e.g., % improvements, number of users)
- Suggest formatting improvements (layout, section order, font consistency)
- Enhance project descriptions with impact-focused, results-driven phrasing
- Use strong action verbs instead of weak, generic verbs

Response Format:
- Return exactly 5 to 6 suggestions.
- Each point should start with a category label followed by a colon. For example:
  - Missing Skill: Add React.js to the skills section...
  - Project Impact: Emphasize how your project benefited users...

Do NOT use asterisks, markdown, stars, or any extra formatting.

---

Job Description:
{jd_text}

Resume:
{resume_text}

Only respond with the bullet point suggestions. No explanations or extra commentary.
"""

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        print(f"AI Suggestion Error: {e}")
        return "❌ Unable to generate AI suggestions at this time."
