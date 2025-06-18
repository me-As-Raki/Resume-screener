# 🧠 Resume Screener — JD Matcher with AI Suggestions 📄🤖

**Screen smarter, not harder!**  
A full-featured Flask web app that automates resume screening by comparing resumes against job descriptions using AI (Gemini), and gives instant match scores, smart suggestions, and visual insights.

---

## 📁 Project Structure

```
resume-screener/
│
├── app/
│   ├── templates/               # HTML templates (login.html, result.html, etc.)
│   ├── static/                  # CSS, JS, and images
│   ├── __init__.py              # App factory
│   ├── models.py                # Database models
│   ├── routes.py                # Flask routes (login, register, upload, etc.)
│   ├── utils.py                 # Resume analysis, AI integration
│   ├── contact_utils.py         # Contact info extraction logic
│   └── email_utils.py           # OTP & email sending utilities
│
├── uploads/                     # Uploaded resumes
├── requirements.txt             # Python dependencies
├── run.py                       # Entry point to run the Flask app
├── .env                         # Environment variables (API keys, secrets)
└── README.md                    # This file
```

---

## 📌 Features

- 🧑‍💼 Role-based login system (HR / Candidate)
- 📄 Upload job description & multiple PDF resumes
- 📊 Match score with matched and missing skills
- 🤖 AI suggestions (OpenAI or Gemini) to improve resumes
- ✅ Auto-shortlisting of resumes based on score
- 🧠 Extracted contact details (name, email, phone)
- 📈 Visual charts (match % pie charts, skill graphs)
- 🌙 Dark mode toggle for clean UI
- 🔒 Secure login with OTP-based "Forgot Password"

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap, Chart.js
- **Backend:** Python, Flask
- **Database:** SQLite (via SQLAlchemy)
- **Authentication:** Flask-Login + OTP email system
- **AI:**  Google Gemini API
- **Deployment Ready:** GitHub, Render, Vercel (optional frontend)

---

## 🚀 How to Run This Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/me-As-Raki/resume-screener.git
cd resume-screener
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Setup your environment variables

Create a `.env` file with this format:

```
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_flask_secret_key
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_email_password_or_app_password
```

### 5. Run the Flask app

```bash
flask run
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧑‍💻 Author

Made with ❤️ by **Rakesh Poojary**  
_Connect with me on [LinkedIn](https://www.linkedin.com/in/rakesh-poojary-127389264)_# Resume-screener
# Resume-screener
