"""
JobResumeChanger - Flask Application
A tool to analyze resumes against job descriptions and enhance them automatically.
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename

from utils.resume_parser import ResumeParser
from utils.job_analyzer import JobAnalyzer
from utils.resume_analyzer import ResumeAnalyzer
from utils.web_search import WebSearcher
from utils.resume_modifier import ResumeModifier

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze uploaded resume against job description.
    Returns missing skills/requirements.
    """
    # Check if resume file is present
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file uploaded'}), 400

    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '').strip()

    if resume_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400

    if not allowed_file(resume_file.filename):
        return jsonify({'error': 'Only PDF and DOCX files are allowed'}), 400

    try:
        # Generate unique session ID for this analysis
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

        # Save uploaded file
        filename = secure_filename(resume_file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        saved_filename = f"{session_id}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        resume_file.save(filepath)

        # Store file info in session
        session['resume_path'] = filepath
        session['original_filename'] = filename
        session['file_ext'] = file_ext

        # Parse resume
        parser = ResumeParser()
        resume_text, resume_sections = parser.parse(filepath)
        session['resume_text'] = resume_text
        session['resume_sections'] = resume_sections

        # Analyze job description
        job_analyzer = JobAnalyzer()
        job_requirements = job_analyzer.analyze(job_description)
        session['job_requirements'] = job_requirements

        # Find missing points in resume
        resume_analyzer = ResumeAnalyzer()
        analysis_result = resume_analyzer.analyze(resume_text, resume_sections, job_requirements)
        session['analysis_result'] = analysis_result

        return jsonify({
            'success': True,
            'session_id': session_id,
            'resume_sections': list(resume_sections.keys()),
            'job_requirements': job_requirements,
            'missing_points': analysis_result['missing_points'],
            'match_score': analysis_result['match_score'],
            'matched_points': analysis_result['matched_points']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['POST'])
def search_info():
    """
    Search the web for information about missing skills/points.
    """
    data = request.get_json()
    missing_point = data.get('missing_point', '')
    context = data.get('context', '')

    if not missing_point:
        return jsonify({'error': 'Missing point is required'}), 400

    try:
        searcher = WebSearcher()
        search_results = searcher.search(missing_point, context)

        return jsonify({
            'success': True,
            'results': search_results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-content', methods=['POST'])
def generate_content():
    """
    Generate resume content for a missing point based on search results.
    """
    data = request.get_json()
    missing_point = data.get('missing_point', '')
    search_info = data.get('search_info', '')
    target_section = data.get('target_section', '')
    project_context = data.get('project_context', '')

    if not missing_point or not target_section:
        return jsonify({'error': 'Missing point and target section are required'}), 400

    try:
        modifier = ResumeModifier()
        generated_content = modifier.generate_content(
            missing_point,
            search_info,
            target_section,
            project_context
        )

        return jsonify({
            'success': True,
            'generated_content': generated_content
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/modify', methods=['POST'])
def modify_resume():
    """
    Apply modifications to the resume and generate updated file.
    """
    data = request.get_json()
    modifications = data.get('modifications', [])

    if not modifications:
        return jsonify({'error': 'No modifications provided'}), 400

    resume_path = session.get('resume_path')
    file_ext = session.get('file_ext')
    session_id = session.get('session_id')

    if not resume_path or not os.path.exists(resume_path):
        return jsonify({'error': 'Resume file not found. Please upload again.'}), 400

    try:
        modifier = ResumeModifier()

        # Generate modified resume
        output_filename = f"modified_{session_id}.{file_ext}"
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], output_filename)

        modifier.apply_modifications(resume_path, output_path, modifications, file_ext)

        session['modified_resume_path'] = output_path

        return jsonify({
            'success': True,
            'download_ready': True,
            'filename': output_filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download')
def download():
    """
    Download the modified resume.
    """
    modified_path = session.get('modified_resume_path')
    original_filename = session.get('original_filename', 'resume')

    if not modified_path or not os.path.exists(modified_path):
        return jsonify({'error': 'Modified resume not found'}), 404

    # Create download filename
    name_part = original_filename.rsplit('.', 1)[0] if '.' in original_filename else original_filename
    ext = modified_path.rsplit('.', 1)[1]
    download_name = f"{name_part}_optimized.{ext}"

    return send_file(
        modified_path,
        as_attachment=True,
        download_name=download_name
    )


@app.route('/cleanup', methods=['POST'])
def cleanup():
    """
    Clean up temporary files for this session.
    """
    try:
        resume_path = session.get('resume_path')
        modified_path = session.get('modified_resume_path')

        if resume_path and os.path.exists(resume_path):
            os.remove(resume_path)

        if modified_path and os.path.exists(modified_path):
            os.remove(modified_path)

        session.clear()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
