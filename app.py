"""
JobResumeChanger - Main Flask Application
This application helps match resumes to job descriptions by:
1. Analyzing job descriptions to extract key requirements
2. Comparing with uploaded resume to find missing points
3. Searching the internet for relevant information
4. Allowing users to specify where to add missing points
5. Generating an updated resume matching the job description
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import os
from werkzeug.utils import secure_filename
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# Security: Ensure secret key is properly configured
if os.environ.get('FLASK_ENV') == 'production' and not os.environ.get('SECRET_KEY'):
    raise ValueError("SECRET_KEY must be set in production environment")

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

# Import our modules
from modules.resume_parser import ResumeParser
from modules.job_analyzer import JobAnalyzer
from modules.comparison_engine import ComparisonEngine
from modules.web_search import WebSearchEngine
from modules.resume_generator import ResumeGenerator

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Handle file upload and job description submission"""
    try:
        # Check if file and job description are present
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not job_description.strip():
            return jsonify({'error': 'Job description is required'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
            file.save(filepath)
            
            # Parse the resume
            parser = ResumeParser()
            resume_data = parser.parse(filepath)
            
            # Analyze job description
            job_analyzer = JobAnalyzer()
            job_requirements = job_analyzer.analyze(job_description)
            
            # Compare resume with job requirements
            comparison_engine = ComparisonEngine()
            missing_points = comparison_engine.find_missing_points(
                resume_data, 
                job_requirements
            )
            
            # Store data in session
            session['resume_data'] = resume_data
            session['job_requirements'] = job_requirements
            session['missing_points'] = missing_points
            session['original_filepath'] = filepath
            session['original_filename'] = filename
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'missing_points': missing_points,
                'resume_sections': resume_data.get('sections', [])
            })
        else:
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT file'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error processing upload: {str(e)}'}), 500


@app.route('/search_point', methods=['POST'])
def search_point():
    """Search the internet for information about a missing point"""
    try:
        data = request.json
        point = data.get('point', '')
        
        if not point:
            return jsonify({'error': 'Point is required'}), 400
        
        # Search for information
        search_engine = WebSearchEngine()
        search_results = search_engine.search(point)
        
        return jsonify({
            'success': True,
            'results': search_results
        })
        
    except Exception as e:
        return jsonify({'error': f'Error searching: {str(e)}'}), 500


@app.route('/add_point', methods=['POST'])
def add_point():
    """Add a missing point to a specific section of the resume"""
    try:
        data = request.json
        point = data.get('point', '')
        section = data.get('section', '')
        project = data.get('project', '')
        additional_info = data.get('additional_info', '')
        
        if not point or not section:
            return jsonify({'error': 'Point and section are required'}), 400
        
        # Get session data
        resume_data = session.get('resume_data', {})
        
        # Add the point to the specified section
        if 'added_points' not in session:
            session['added_points'] = []
        
        added_point = {
            'point': point,
            'section': section,
            'project': project,
            'additional_info': additional_info,
            'timestamp': datetime.now().isoformat()
        }
        
        session['added_points'].append(added_point)
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Point added successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error adding point: {str(e)}'}), 500


@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    """Generate the updated resume with all added points"""
    try:
        # Get session data
        resume_data = session.get('resume_data', {})
        added_points = session.get('added_points', [])
        original_filepath = session.get('original_filepath', '')
        session_id = session.get('session_id', '')
        
        if not resume_data or not added_points:
            return jsonify({'error': 'No data available to generate resume'}), 400
        
        # Generate updated resume
        generator = ResumeGenerator()
        output_filepath = os.path.join(
            app.config['PROCESSED_FOLDER'], 
            f"{session_id}_updated_resume.pdf"
        )
        
        generator.generate(
            resume_data,
            added_points,
            original_filepath,
            output_filepath
        )
        
        session['updated_resume_path'] = output_filepath
        
        return jsonify({
            'success': True,
            'message': 'Resume generated successfully',
            'download_url': '/download'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error generating resume: {str(e)}'}), 500


@app.route('/download')
def download():
    """Download the updated resume"""
    try:
        updated_resume_path = session.get('updated_resume_path', '')
        
        if not updated_resume_path or not os.path.exists(updated_resume_path):
            return jsonify({'error': 'No updated resume available'}), 404
        
        return send_file(
            updated_resume_path,
            as_attachment=True,
            download_name='updated_resume.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error downloading resume: {str(e)}'}), 500


@app.route('/status')
def status():
    """Get current session status"""
    try:
        return jsonify({
            'has_session': 'session_id' in session,
            'session_id': session.get('session_id', ''),
            'missing_points_count': len(session.get('missing_points', [])),
            'added_points_count': len(session.get('added_points', []))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
