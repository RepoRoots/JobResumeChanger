"""
JobResumeChanger - Main Flask Application
This application helps match resumes to job descriptions by:
1. Analyzing job descriptions to extract key requirements
2. Comparing with uploaded resume to find missing points
3. Searching the internet for relevant information
4. Allowing users to specify where to add missing points
5. Generating an updated resume matching the job description

Refactored to follow Object-Oriented Programming principles with:
- Service layer for business logic
- Separation of concerns
- Dependency injection
- Controller pattern for routes
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import os
from typing import Tuple, Optional

from services.resume_service import ResumeService
from services.session_service import SessionService


class ApplicationConfig:
    """Configuration class for application settings"""
    
    def __init__(self):
        self.upload_folder = 'uploads'
        self.processed_folder = 'processed'
        self.max_content_length = 16 * 1024 * 1024  # 16MB
        self.allowed_extensions = {'pdf', 'docx', 'txt'}
        self.secret_key = self._get_secret_key()
    
    @staticmethod
    def _get_secret_key() -> str:
        """Get secret key from environment with validation"""
        if os.environ.get('FLASK_ENV') == 'production' and not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY must be set in production environment")
        return os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


class ResumeController:
    """Controller class for handling resume-related routes"""
    
    def __init__(self, resume_service: ResumeService, session_service: SessionService):
        """
        Initialize the controller with required services
        
        Args:
            resume_service: Service for resume operations
            session_service: Service for session management
        """
        self.resume_service = resume_service
        self.session_service = session_service
    
    def upload(self) -> Tuple[dict, int]:
        """
        Handle file upload and job description submission
        
        Returns:
            Tuple of (response dict, status code)
        """
        try:
            # Validate request
            if 'resume' not in request.files:
                return {'error': 'No resume file uploaded'}, 400
            
            file = request.files['resume']
            job_description = request.form.get('job_description', '')
            
            # Process the upload
            result = self.resume_service.process_resume_upload(file, job_description)
            
            # Initialize session
            self.session_service.initialize_session(
                result['session_id'],
                result['resume_data'],
                result['job_requirements'],
                result['missing_points'],
                result['filepath'],
                result['filename']
            )
            
            return {
                'success': True,
                'session_id': result['session_id'],
                'missing_points': result['missing_points'],
                'resume_sections': result['resume_data'].get('sections', [])
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Error processing upload: {str(e)}'}, 500
    
    def search_point(self) -> Tuple[dict, int]:
        """
        Search for suggestions about a missing point
        
        Returns:
            Tuple of (response dict, status code)
        """
        try:
            data = request.json
            point = data.get('point', '')
            
            # Search for suggestions
            results = self.resume_service.search_suggestions(point)
            
            return {
                'success': True,
                'results': results
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Error searching: {str(e)}'}, 500
    
    def add_point(self) -> Tuple[dict, int]:
        """
        Add a missing point to a specific section of the resume
        
        Returns:
            Tuple of (response dict, status code)
        """
        try:
            data = request.json
            point = data.get('point', '')
            section = data.get('section', '')
            project = data.get('project', '')
            additional_info = data.get('additional_info', '')
            
            if not point or not section:
                return {'error': 'Point and section are required'}, 400
            
            # Add point to session
            self.session_service.add_point(point, section, project, additional_info)
            
            return {
                'success': True,
                'message': 'Point added successfully'
            }, 200
            
        except Exception as e:
            return {'error': f'Error adding point: {str(e)}'}, 500
    
    def generate_resume(self) -> Tuple[dict, int]:
        """
        Generate the updated resume with all added points
        
        Returns:
            Tuple of (response dict, status code)
        """
        try:
            # Get data from session
            resume_data = self.session_service.get_resume_data()
            added_points = self.session_service.get_added_points()
            original_filepath = self.session_service.get_original_filepath()
            session_id = self.session_service.get_session_id()
            
            if not resume_data or not added_points:
                return {'error': 'No data available to generate resume'}, 400
            
            # Generate updated resume
            output_filepath = self.resume_service.generate_updated_resume(
                resume_data,
                added_points,
                original_filepath,
                session_id
            )
            
            # Store path in session
            self.session_service.set_updated_resume_path(output_filepath)
            
            return {
                'success': True,
                'message': 'Resume generated successfully',
                'download_url': '/download'
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Error generating resume: {str(e)}'}, 500
    
    def download(self):
        """
        Download the updated resume
        
        Returns:
            File response or error dict with status code
        """
        try:
            updated_resume_path = self.session_service.get_updated_resume_path()
            
            if not self.resume_service.validate_file_exists(updated_resume_path):
                return {'error': 'No updated resume available'}, 404
            
            return send_file(
                updated_resume_path,
                as_attachment=True,
                download_name='updated_resume.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            return {'error': f'Error downloading resume: {str(e)}'}, 500
    
    def get_status(self) -> Tuple[dict, int]:
        """
        Get current session status
        
        Returns:
            Tuple of (status dict, status code)
        """
        try:
            return self.session_service.get_status(), 200
        except Exception as e:
            return {'error': str(e)}, 500
    
    def check_ats_score(self) -> Tuple[dict, int]:
        """
        Check ATS compliance score for uploaded resume
        
        Returns:
            Tuple of (ATS score dict, status code)
        """
        try:
            # Get data from session
            resume_data = self.session_service.get_resume_data()
            job_requirements = self.session_service.get_job_requirements()
            
            if not resume_data:
                return {'error': 'No resume data available'}, 400
            
            # Calculate ATS score
            ats_score = self.resume_service.check_ats_score(resume_data, job_requirements)
            
            return {
                'success': True,
                'ats_score': ats_score
            }, 200
            
        except Exception as e:
            return {'error': f'Error checking ATS score: {str(e)}'}, 500
    
    def optimize_resume(self) -> Tuple[dict, int]:
        """
        Get optimization suggestions for ATS compliance
        
        Returns:
            Tuple of (optimization suggestions dict, status code)
        """
        try:
            # Get data from session
            resume_data = self.session_service.get_resume_data()
            job_requirements = self.session_service.get_job_requirements()
            
            if not resume_data:
                return {'error': 'No resume data available'}, 400
            
            # Get optimization suggestions
            suggestions = self.resume_service.get_optimization_suggestions(
                resume_data, job_requirements
            )
            
            return {
                'success': True,
                'suggestions': suggestions
            }, 200
            
        except Exception as e:
            return {'error': f'Error getting optimization suggestions: {str(e)}'}, 500


class JobResumeChangerApp:
    """Main application class following OOP principles"""
    
    def __init__(self, config: ApplicationConfig):
        """
        Initialize the application with configuration
        
        Args:
            config: Application configuration object
        """
        self.config = config
        self.app = Flask(__name__)
        self._configure_app()
        self._initialize_services()
        self._register_routes()
    
    def _configure_app(self) -> None:
        """Configure Flask application"""
        self.app.secret_key = self.config.secret_key
        self.app.config['UPLOAD_FOLDER'] = self.config.upload_folder
        self.app.config['PROCESSED_FOLDER'] = self.config.processed_folder
        self.app.config['MAX_CONTENT_LENGTH'] = self.config.max_content_length
        self.app.config['ALLOWED_EXTENSIONS'] = self.config.allowed_extensions
    
    def _initialize_services(self) -> None:
        """Initialize service layer objects"""
        self.resume_service = ResumeService(
            self.config.upload_folder,
            self.config.processed_folder,
            self.config.allowed_extensions
        )
    
    def _get_session_service(self) -> SessionService:
        """
        Get session service for current request
        
        Returns:
            SessionService instance for current session
        """
        return SessionService(session)
    
    def _register_routes(self) -> None:
        """Register all application routes"""
        
        @self.app.route('/')
        def index():
            """Main page with upload form"""
            return render_template('index.html')
        
        @self.app.route('/upload', methods=['POST'])
        def upload():
            """Handle file upload and job description submission"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status = controller.upload()
            return jsonify(response), status
        
        @self.app.route('/search_point', methods=['POST'])
        def search_point():
            """Search the internet for information about a missing point"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status = controller.search_point()
            return jsonify(response), status
        
        @self.app.route('/add_point', methods=['POST'])
        def add_point():
            """Add a missing point to a specific section of the resume"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status = controller.add_point()
            return jsonify(response), status
        
        @self.app.route('/generate_resume', methods=['POST'])
        def generate_resume():
            """Generate the updated resume with all added points"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status = controller.generate_resume()
            return jsonify(response), status
        
        @self.app.route('/download')
        def download():
            """Download the updated resume"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            return controller.download()
        
        @self.app.route('/status')
        def status():
            """Get current session status"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status_code = controller.get_status()
            return jsonify(response), status_code
        
        @self.app.route('/check_ats_score', methods=['POST'])
        def check_ats_score():
            """Check ATS compliance score"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status = controller.check_ats_score()
            return jsonify(response), status
        
        @self.app.route('/optimize_resume', methods=['POST'])
        def optimize_resume():
            """Get optimization suggestions for ATS compliance"""
            controller = ResumeController(self.resume_service, self._get_session_service())
            response, status = controller.optimize_resume()
            return jsonify(response), status
    
    def run(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        """
        Run the Flask application
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        # Only enable debug mode in development
        debug_mode = os.environ.get('FLASK_ENV') != 'production'
        self.app.run(debug=debug_mode, host=host, port=port)


def create_app() -> Flask:
    """
    Application factory function
    
    Returns:
        Configured Flask application
    """
    config = ApplicationConfig()
    app_instance = JobResumeChangerApp(config)
    return app_instance.app


# Create global app instance for WSGI servers
app = create_app()


if __name__ == '__main__':
    # Create and run the application
    config = ApplicationConfig()
    application = JobResumeChangerApp(config)
    application.run()
