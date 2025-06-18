from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ----------------------
# User Model
# ----------------------
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'hr' or 'candidate'
    # In User model
    reset_otp = db.Column(db.String(6))        # Optional: temporary OTP
    otp_expiry = db.Column(db.DateTime)        # Optional: expiry time for OTP


    # Relationship to Result model
    results = db.relationship('Result', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.id} - {self.email}>'


# ----------------------
# Result (Analysis) Model
# ----------------------
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matched_skills = db.Column(db.Text, nullable=False)
    missing_skills = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Integer, nullable=False)
    jd_text = db.Column(db.Text, nullable=False)
    resume_filename = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'shortlisted' or 'rejected'

    # ✅ Contact info extracted from resume
    extracted_name = db.Column(db.String(100))
    extracted_email = db.Column(db.String(150))
    extracted_phone = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Result {self.id} - Score: {self.match_score}%>'
