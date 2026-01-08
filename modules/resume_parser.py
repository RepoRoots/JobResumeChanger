"""
Resume Parser Module
Extracts text and structure from resume files (PDF, DOCX, TXT)
"""

import os
import re
from typing import Dict, List


class ResumeParser:
    """Parse resume files and extract structured information"""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'docx', 'txt']
    
    def parse(self, filepath: str) -> Dict:
        """
        Parse a resume file and extract structured data
        
        Args:
            filepath: Path to the resume file
            
        Returns:
            Dictionary containing parsed resume data
        """
        file_extension = filepath.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            text = self._parse_pdf(filepath)
        elif file_extension == 'docx':
            text = self._parse_docx(filepath)
        elif file_extension == 'txt':
            text = self._parse_txt(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Extract structured information
        structured_data = self._extract_structure(text)
        structured_data['raw_text'] = text
        
        return structured_data
    
    def _parse_pdf(self, filepath: str) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            
            text = ""
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            # Fallback if PyPDF2 is not available
            return self._simple_text_extraction(filepath)
    
    def _parse_docx(self, filepath: str) -> str:
        """Extract text from DOCX file"""
        try:
            from docx import Document
            
            doc = Document(filepath)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except ImportError:
            # Fallback if python-docx is not available
            return self._simple_text_extraction(filepath)
    
    def _parse_txt(self, filepath: str) -> str:
        """Extract text from TXT file"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    def _simple_text_extraction(self, filepath: str) -> str:
        """Simple text extraction fallback"""
        with open(filepath, 'rb') as file:
            content = file.read()
            # Try to decode as text
            try:
                return content.decode('utf-8', errors='ignore')
            except:
                return content.decode('latin-1', errors='ignore')
    
    def _extract_structure(self, text: str) -> Dict:
        """
        Extract structured information from resume text
        
        Returns:
            Dictionary with sections, skills, experience, education, etc.
        """
        sections = self._identify_sections(text)
        skills = self._extract_skills(text)
        experience = self._extract_experience(text)
        education = self._extract_education(text)
        
        return {
            'sections': sections,
            'skills': skills,
            'experience': experience,
            'education': education
        }
    
    def _identify_sections(self, text: str) -> List[Dict]:
        """Identify major sections in the resume"""
        sections = []
        
        # Common section headers
        section_patterns = [
            r'(?i)^(SUMMARY|OBJECTIVE|PROFILE)',
            r'(?i)^(EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT)',
            r'(?i)^(EDUCATION|ACADEMIC BACKGROUND)',
            r'(?i)^(SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES)',
            r'(?i)^(PROJECTS|KEY PROJECTS)',
            r'(?i)^(CERTIFICATIONS|CERTIFICATES)',
            r'(?i)^(ACHIEVEMENTS|ACCOMPLISHMENTS)',
            r'(?i)^(AWARDS|HONORS)',
        ]
        
        lines = text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            is_header = False
            for pattern in section_patterns:
                if re.match(pattern, line):
                    # Save previous section
                    if current_section:
                        sections.append({
                            'name': current_section,
                            'content': '\n'.join(section_content)
                        })
                    
                    current_section = line
                    section_content = []
                    is_header = True
                    break
            
            if not is_header and current_section:
                section_content.append(line)
        
        # Add last section
        if current_section:
            sections.append({
                'name': current_section,
                'content': '\n'.join(section_content)
            })
        
        # If no sections found, create a default one
        if not sections:
            sections.append({
                'name': 'Content',
                'content': text
            })
        
        return sections
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        
        # Common technical skills patterns
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'C\\+\\+', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
            'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'NLP',
            'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum'
        ]
        
        text_lower = text.lower()
        for skill in skill_keywords:
            # Handle special characters in skill names
            if skill == 'C\\+\\+':
                # Special case for C++ - use lookahead/lookbehind for word boundaries
                if re.search(r'(?<![a-z])c\+\+(?![a-z])', text_lower):
                    skills.append('C++')
            elif skill == 'C#':
                # Special case for C#
                if re.search(r'(?<![a-z])c#(?![a-z])', text_lower):
                    skills.append('C#')
            else:
                # Regular matching for other skills
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                    skills.append(skill)
        
        return skills
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience entries"""
        experience = []
        
        # Look for experience section
        exp_match = re.search(
            r'(?i)(EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE)(.*?)(?=(EDUCATION|SKILLS|PROJECTS|CERTIFICATIONS|$))',
            text,
            re.DOTALL
        )
        
        if exp_match:
            exp_text = exp_match.group(2)
            # Split by common date patterns or company indicators
            entries = re.split(r'\n(?=\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))', exp_text)
            
            for entry in entries:
                entry = entry.strip()
                if entry and len(entry) > 20:  # Filter out very short entries
                    experience.append({
                        'text': entry,
                        'type': 'work_experience'
                    })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education entries"""
        education = []
        
        # Look for education section
        edu_match = re.search(
            r'(?i)(EDUCATION|ACADEMIC BACKGROUND)(.*?)(?=(EXPERIENCE|SKILLS|PROJECTS|CERTIFICATIONS|$))',
            text,
            re.DOTALL
        )
        
        if edu_match:
            edu_text = edu_match.group(2)
            lines = [line.strip() for line in edu_text.split('\n') if line.strip()]
            
            for line in lines:
                if len(line) > 10:  # Filter out very short lines
                    education.append({
                        'text': line,
                        'type': 'education'
                    })
        
        return education
