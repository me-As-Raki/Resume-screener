from models import AnalysisResult
from flask_login import current_user

# Inside your route after analysis
result = AnalysisResult(
    user_id=current_user.id,
    score=final_score,
    matched_skills=",".join(matched_skills),
    missing_skills=",".join(missing_skills),
    resume_filename=uploaded_resume_filename
)
db.session.add(result)
db.session.commit()
