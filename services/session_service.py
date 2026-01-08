"""
Session Service
Manages user session data following OOP principles
"""

from typing import Dict, Optional, Any
from datetime import datetime


class SessionService:
    """Service class for managing session state"""
    
    def __init__(self, session_store):
        """
        Initialize the Session Service
        
        Args:
            session_store: Flask session object or similar session storage
        """
        self.session = session_store
    
    def initialize_session(self, session_id: str, resume_data: Dict,
                          job_requirements: Dict, missing_points: list,
                          filepath: str, filename: str) -> None:
        """
        Initialize session with resume analysis data
        
        Args:
            session_id: Unique session identifier
            resume_data: Parsed resume data
            job_requirements: Analyzed job requirements
            missing_points: List of missing points
            filepath: Path to uploaded file
            filename: Original filename
        """
        self.session['session_id'] = session_id
        self.session['resume_data'] = resume_data
        self.session['job_requirements'] = job_requirements
        self.session['missing_points'] = missing_points
        self.session['original_filepath'] = filepath
        self.session['original_filename'] = filename
        self.session['added_points'] = []
        self.session['created_at'] = datetime.now().isoformat()
    
    def add_point(self, point: str, section: str, project: str = '',
                  additional_info: str = '') -> Dict:
        """
        Add a point to the session
        
        Args:
            point: The point to add
            section: Resume section for the point
            project: Optional project name
            additional_info: Optional additional information
            
        Returns:
            The added point data
        """
        if 'added_points' not in self.session:
            self.session['added_points'] = []
        
        added_point = {
            'point': point,
            'section': section,
            'project': project,
            'additional_info': additional_info,
            'timestamp': datetime.now().isoformat()
        }
        
        self.session['added_points'].append(added_point)
        self.session.modified = True
        
        return added_point
    
    def get_resume_data(self) -> Optional[Dict]:
        """Get resume data from session"""
        return self.session.get('resume_data')
    
    def get_job_requirements(self) -> Optional[Dict]:
        """Get job requirements from session"""
        return self.session.get('job_requirements')
    
    def get_missing_points(self) -> list:
        """Get missing points from session"""
        return self.session.get('missing_points', [])
    
    def get_added_points(self) -> list:
        """Get added points from session"""
        return self.session.get('added_points', [])
    
    def get_original_filepath(self) -> Optional[str]:
        """Get original file path from session"""
        return self.session.get('original_filepath')
    
    def set_updated_resume_path(self, path: str) -> None:
        """
        Set the path to the updated resume
        
        Args:
            path: Path to updated resume file
        """
        self.session['updated_resume_path'] = path
        self.session.modified = True
    
    def get_updated_resume_path(self) -> Optional[str]:
        """Get updated resume path from session"""
        return self.session.get('updated_resume_path')
    
    def get_session_id(self) -> Optional[str]:
        """Get session ID"""
        return self.session.get('session_id')
    
    def has_session(self) -> bool:
        """Check if session exists"""
        return 'session_id' in self.session
    
    def get_status(self) -> Dict:
        """
        Get session status information
        
        Returns:
            Dictionary with session status
        """
        return {
            'has_session': self.has_session(),
            'session_id': self.get_session_id() or '',
            'missing_points_count': len(self.get_missing_points()),
            'added_points_count': len(self.get_added_points())
        }
    
    def clear_session(self) -> None:
        """Clear all session data"""
        self.session.clear()
