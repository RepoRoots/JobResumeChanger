"""
Resume Service
Handles all resume-related business logic following OOP principles
"""

import os
import uuid
from typing import Dict, Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from modules.resume_parser import ResumeParser
from modules.job_analyzer import JobAnalyzer
from modules.comparison_engine import ComparisonEngine
from modules.web_search import WebSearchEngine
from modules.resume_generator import ResumeGenerator
from modules.ats_checker import ATSChecker


class ResumeService:
    """Service class for handling resume operations"""
    
    def __init__(self, upload_folder: str, processed_folder: str, allowed_extensions: set):
        """
        Initialize the Resume Service
        
        Args:
            upload_folder: Directory for uploaded files
            processed_folder: Directory for processed files
            allowed_extensions: Set of allowed file extensions
        """
        self.upload_folder = upload_folder
        self.processed_folder = processed_folder
        self.allowed_extensions = allowed_extensions
        
        # Initialize module instances
        self.resume_parser = ResumeParser()
        self.job_analyzer = JobAnalyzer()
        self.comparison_engine = ComparisonEngine()
        self.web_search_engine = WebSearchEngine()
        self.resume_generator = ResumeGenerator()
        self.ats_checker = ATSChecker()
        
        # Ensure directories exist
        os.makedirs(self.upload_folder, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
    
    def is_allowed_file(self, filename: str) -> bool:
        """
        Check if the file extension is allowed
        
        Args:
            filename: Name of the file
            
        Returns:
            True if file extension is allowed, False otherwise
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def process_resume_upload(self, file: FileStorage, job_description: str) -> Dict:
        """
        Process uploaded resume and job description
        
        Args:
            file: Uploaded resume file
            job_description: Job description text
            
        Returns:
            Dictionary containing analysis results
            
        Raises:
            ValueError: If file or job description is invalid
        """
        # Validate inputs
        if not file or file.filename == '':
            raise ValueError('No file selected')
        
        if not job_description.strip():
            raise ValueError('Job description is required')
        
        if not self.is_allowed_file(file.filename):
            raise ValueError('Invalid file type. Please upload PDF, DOCX, or TXT file')
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_folder, f"{session_id}_{filename}")
        file.save(filepath)
        
        # Parse the resume
        resume_data = self.resume_parser.parse(filepath)
        
        # Analyze job description
        job_requirements = self.job_analyzer.analyze(job_description)
        
        # Compare resume with job requirements
        missing_points = self.comparison_engine.find_missing_points(
            resume_data,
            job_requirements
        )
        
        return {
            'session_id': session_id,
            'filepath': filepath,
            'filename': filename,
            'resume_data': resume_data,
            'job_requirements': job_requirements,
            'missing_points': missing_points
        }
    
    def search_suggestions(self, point: str) -> list:
        """
        Search for suggestions about a missing point
        
        Args:
            point: The missing point to search for
            
        Returns:
            List of search suggestions
            
        Raises:
            ValueError: If point is empty
        """
        if not point:
            raise ValueError('Point is required')
        
        return self.web_search_engine.search(point)
    
    def generate_updated_resume(self, resume_data: Dict, added_points: list,
                               original_filepath: str, session_id: str) -> str:
        """
        Generate an updated resume with added points
        
        Args:
            resume_data: Original resume data
            added_points: List of points to add
            original_filepath: Path to original resume
            session_id: Session identifier
            
        Returns:
            Path to generated resume file
            
        Raises:
            ValueError: If required data is missing
        """
        if not resume_data or not added_points:
            raise ValueError('Resume data and added points are required')
        
        # Generate output filepath
        output_filepath = os.path.join(
            self.processed_folder,
            f"{session_id}_updated_resume.pdf"
        )
        
        # Generate the resume
        self.resume_generator.generate(
            resume_data,
            added_points,
            original_filepath,
            output_filepath
        )
        
        return output_filepath
    
    def validate_file_exists(self, filepath: str) -> bool:
        """
        Validate that a file exists
        
        Args:
            filepath: Path to file
            
        Returns:
            True if file exists, False otherwise
        """
        return filepath and os.path.exists(filepath)
    
    def check_ats_score(self, resume_data: Dict, job_requirements: Dict = None) -> Dict:
        """
        Check ATS compliance score for a resume
        
        Args:
            resume_data: Parsed resume data
            job_requirements: Optional job requirements for keyword matching
            
        Returns:
            Dictionary containing ATS score and recommendations
        """
        return self.ats_checker.calculate_ats_score(resume_data, job_requirements)
    
    def get_optimization_suggestions(self, resume_data: Dict, 
                                    job_requirements: Dict = None) -> Dict:
        """
        Get optimization suggestions for improving ATS score
        
        Args:
            resume_data: Parsed resume data
            job_requirements: Optional job requirements
            
        Returns:
            Dictionary with categorized optimization suggestions
        """
        return self.ats_checker.generate_optimization_suggestions(
            resume_data, job_requirements
        )
