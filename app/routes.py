import traceback
from flask import jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Result
from app.utils import extract_text_from_pdf, analyze_resume, generate_ai_suggestions, send_email
from app.contact_utils import extract_contact_details
import os
import random
from flask import session
from app.email_utils import send_otp_email  # you'll create this soon

main = Blueprint('main', __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------- REGISTER --------------------
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        print("📝 Register attempt received")
        print(f"👉 Name: {name}, Email: {email}, Role: {role}")

        if not name or not email or not password or not role:
            print("❌ Missing required fields during registration")
            flash('All fields are required.')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"⚠️ Email already registered: {email}")
            flash('Email already registered.')
            return redirect(url_for('main.register'))

        try:
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"✅ New user registered: {email}")
            flash('Registered successfully. Please login.')
            return redirect(url_for('main.login'))
        except Exception as e:
            print("❌ Exception during registration:")
            traceback.print_exc()
            flash('An error occurred during registration.')
            return redirect(url_for('main.register'))

    print("📄 Rendering registration page")
    return render_template('register.html')

# -------------------- LOGIN --------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print("🔐 Login attempt received")
        print(f"👉 Email: {email}")

        if not email or not password:
            print("❌ Missing email or password in login")
            flash('Email and password are required.')
            return redirect(url_for('main.login'))

        try:
            user = User.query.filter_by(email=email).first()

            if user:
                print(f"👤 Found user in DB: {user.email}")
                if user.check_password(password):
                    print(f"✅ Login successful for: {email}")
                    login_user(user)
                    flash(f'Welcome {user.name}!')
                    return redirect(url_for('main.dashboard'))
                else:
                    print("❌ Incorrect password")
                    flash('Invalid email or password.')
            else:
                print("❌ No user found with that email")
                flash('Invalid email or password.')
        except Exception as e:
            print("❌ Exception during login:")
            traceback.print_exc()
            flash('An error occurred during login.')
            return redirect(url_for('main.login'))

    print("📄 Rendering login page")
    return render_template('login.html')
# -------------------- ROOT PAGE --------------------
@main.route('/')
def root():
    return redirect(url_for('main.login'))

# -------------------- LOGOUT --------------------
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

# -------------------- DASHBOARD --------------------
@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'hr':
        return render_template('hr_dashboard.html', user=current_user)
    else:
        return render_template('dashboard.html', user=current_user)

# -------------------- CANDIDATE: ANALYZE --------------------
@main.route('/analyze', methods=['POST'])
@login_required
def analyze():
    resume_file = request.files['resume']
    jd_text = request.form['jd_text']

    if not resume_file or not jd_text:
        flash("Please upload a resume and paste a job description.")
        return redirect(url_for('main.dashboard'))

    # Step 1: Extract text and contact info
    resume_text = extract_text_from_pdf(resume_file)
    result_data = analyze_resume(resume_text, jd_text)
    name, email, phone = extract_contact_details(resume_text)

    # Step 2: Determine shortlist status
    status = 'shortlisted' if result_data['score'] >= 75 else 'rejected'

    # Step 3: AI Suggestions
    from app.utils import generate_ai_suggestions  # Ensure import if not already
    suggestions = generate_ai_suggestions(resume_text, jd_text)

    # Optional: Debug in terminal
    print("===== AI Resume Suggestions =====")
    print(suggestions)
    print("=================================")

    # Step 4: Save result to DB
    new_result = Result(
        matched_skills=", ".join(result_data['matched']),
        missing_skills=", ".join(result_data['missing']),
        match_score=result_data['score'],
        jd_text=jd_text,
        resume_filename=resume_file.filename,
        status=status,
        extracted_name=name,
        extracted_email=email,
        extracted_phone=phone,
        user=current_user
    )
    db.session.add(new_result)
    db.session.commit()

    # Step 5: Render the result template
    return render_template(
        'result.html',
        result=result_data,
        name=current_user.name,
        suggestions=suggestions
    )



# -------------------- HR: BULK ANALYZE --------------------
@main.route('/hr-bulk-analyze', methods=['GET', 'POST'])
@login_required
def hr_bulk_analyze():
    if current_user.role != 'hr':
        flash("Access denied.")
        return redirect(url_for('main.dashboard'))

    if request.method == 'GET':
        results = Result.query.filter_by(user_id=current_user.id).all()
        return render_template('hr_results.html', results=[{
            "id": r.id,
            "filename": r.resume_filename,
            "score": r.match_score,
            "matched": r.matched_skills.split(', '),
            "missing": r.missing_skills.split(', '),
            "status": r.status,
            "email": r.extracted_email,
            "name": r.extracted_name,
            "phone": r.extracted_phone
        } for r in results], jd_text="")

    jd_text = request.form.get('jd_text', '')
    filter_type = request.form.get('filter')

    if filter_type == 'shortlisted':
        shortlisted_results = Result.query.filter_by(user_id=current_user.id, status='shortlisted').all()
        return render_template('hr_results.html', results=[{
            "id": r.id,
            "filename": r.resume_filename,
            "score": r.match_score,
            "matched": r.matched_skills.split(', '),
            "missing": r.missing_skills.split(', '),
            "status": r.status,
            "email": r.extracted_email,
            "name": r.extracted_name,
            "phone": r.extracted_phone
        } for r in shortlisted_results], jd_text=jd_text)

    resume_files = request.files.getlist('resumes')
    if not resume_files or not jd_text:
        flash("Please upload resumes and provide a job description.")
        return redirect(url_for('main.dashboard'))

    results = []
    for resume in resume_files:
        filename = secure_filename(resume.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        resume.save(save_path)

        with open(save_path, 'rb') as f:
            resume_text = extract_text_from_pdf(f)

        result_data = analyze_resume(resume_text, jd_text)
        name, email, phone = extract_contact_details(resume_text)
        status = 'shortlisted' if result_data['score'] >= 75 else 'rejected'

        new_result = Result(
            matched_skills=", ".join(result_data['matched']),
            missing_skills=", ".join(result_data['missing']),
            match_score=result_data['score'],
            jd_text=jd_text,
            resume_filename=filename,
            status=status,
            extracted_name=name,
            extracted_email=email,
            extracted_phone=phone,
            user=current_user
        )
        db.session.add(new_result)
        db.session.commit()

        results.append({
            "id": new_result.id,
            "filename": filename,
            "score": result_data['score'],
            "matched": result_data['matched'],
            "missing": result_data['missing'],
            "status": status,
            "email": email,
            "name": name,
            "phone": phone
        })

    return render_template('hr_results.html', results=results, jd_text=jd_text)

# -------------------- MANUAL SHORTLIST --------------------
@main.route('/shortlist/<int:result_id>', methods=['POST'])
@login_required
def shortlist_result(result_id):
    result = Result.query.get_or_404(result_id)

    if current_user.role != 'hr' or result.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    result.status = "shortlisted"
    db.session.commit()
    
    return jsonify({'success': True})


# -------------------- SEND MESSAGE TO SHORTLISTED --------------------
@main.route('/send_hr_message', methods=['POST'])
@login_required
def send_hr_message():
    if current_user.role != 'hr':
        flash("Access denied.")
        return redirect(url_for('main.dashboard'))

    # Step 1: Get all shortlisted candidates for this HR
    shortlisted = Result.query.filter_by(status="shortlisted", user_id=current_user.id).all()

    # Step 2: Filter only those with valid email
    valid_candidates = [res for res in shortlisted if res.extracted_email and '@' in res.extracted_email]

    # 🛠️ Check BEFORE using 'sent_to'
    if not valid_candidates:
        flash("❌ No valid email addresses found among shortlisted candidates.", "warning")
        return render_template("message_confirmation.html", recipients=[])

    # Step 3: Send email and update status
    sent_to = []
    for res in valid_candidates:
        subject = "🎉 You're Shortlisted!"
        body = f"""
Dear {res.extracted_name or 'Candidate'},

Congratulations! 🎉 Your resume has been shortlisted based on the job requirements.

📊 Match Score: {res.match_score}%
📄 Resume: {res.resume_filename}
📞 Contact: {res.extracted_phone or 'N/A'}

We will get in touch with you shortly for the next steps.

Best regards,  
HR Team
"""
        try:
            send_email(res.extracted_email, subject, body)
            res.status = "message_sent"

            sent_to.append({
                "filename": res.resume_filename,
                "name": res.extracted_name,
                "email": res.extracted_email,
                "phone": res.extracted_phone,
                "score": res.match_score
            })
        except Exception as e:
            print(f"Error sending email to {res.extracted_email}: {e}")

    db.session.commit()

    flash(f"✅ Messages sent to {len(sent_to)} candidates.", "success")

    return render_template("message_confirmation.html", recipients=sent_to)



@main.route('/messaged-candidates')
@login_required
def view_messaged_candidates():
    if current_user.role != 'hr':
        return redirect(url_for('main.dashboard'))

    # Get all results where status is 'message_sent' for the current HR
    messaged = Result.query.filter_by(
        user_id=current_user.id,
        status='message_sent'
    ).order_by(Result.timestamp.desc()).all()

    return render_template('messaged_candidates.html', results=messaged)



@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            session['reset_email'] = email
            session['otp'] = otp
            send_otp_email(email, otp)  # This sends the OTP to user's email
            return redirect(url_for('main.verify_otp'))
        else:
            flash('Email not registered', 'danger')
    return render_template('forgot_password.html')

@main.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if 'otp' in session and entered_otp == session['otp']:
            return redirect(url_for('main.reset_password'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    return render_template('verify_otp.html')

@main.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        flash("Unauthorized access. Please start from 'Forgot Password'.", 'danger')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        new_password = request.form['password']

        user = User.query.filter_by(email=session['reset_email']).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            session.pop('reset_email', None)
            session.pop('otp', None)
            flash('Password reset successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('User not found.', 'danger')

    return render_template('reset_password.html')

