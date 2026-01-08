"""
Job Analyzer Module
Analyzes job descriptions to extract key requirements, skills, and qualifications
"""

import re
from typing import Dict, List


class JobAnalyzer:
    """Analyze job descriptions to extract requirements"""
    
    def __init__(self):
        self.requirement_keywords = [
            'required', 'must have', 'should have', 'need', 'looking for',
            'responsibilities', 'qualifications', 'requirements', 'preferred'
        ]
    
    def analyze(self, job_description: str) -> Dict:
        """
        Analyze a job description and extract key information
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary containing extracted requirements
        """
        requirements = {
            'all_requirements': self._extract_requirements(job_description),
            'technical_skills': self._extract_technical_skills(job_description),
            'soft_skills': self._extract_soft_skills(job_description),
            'experience_level': self._extract_experience_level(job_description),
            'education': self._extract_education_requirements(job_description),
            'responsibilities': self._extract_responsibilities(job_description),
            'raw_text': job_description
        }
        
        return requirements
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract all requirement statements from job description"""
        requirements = []
        
        # Split into sentences
        sentences = re.split(r'[.!?\n]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if sentence contains requirement keywords
            sentence_lower = sentence.lower()
            for keyword in self.requirement_keywords:
                if keyword in sentence_lower:
                    requirements.append(sentence)
                    break
        
        # Also extract bullet points
        bullet_points = re.findall(r'[•\-\*]\s*(.+?)(?=[•\-\*]|$)', text, re.MULTILINE)
        requirements.extend([point.strip() for point in bullet_points if point.strip()])
        
        return list(set(requirements))  # Remove duplicates
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills mentioned in the job description"""
        technical_skills = []
        
        # Common technical skills and technologies
        tech_keywords = [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C\\+\\+', 'C#', 'Ruby', 'PHP',
            'Swift', 'Kotlin', 'Go', 'Rust', 'Scala', 'R', 'MATLAB',
            
            # Web Technologies
            'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
            'Spring', 'Express', 'jQuery', 'Bootstrap', 'Webpack', 'Redux',
            
            # Databases
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle',
            'DynamoDB', 'Elasticsearch', 'SQLite',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins',
            'CI/CD', 'Terraform', 'Ansible', 'Linux', 'Unix',
            
            # Data & AI
            'Machine Learning', 'Deep Learning', 'AI', 'Artificial Intelligence',
            'Data Science', 'NLP', 'Natural Language Processing', 'TensorFlow',
            'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            
            # Other
            'REST API', 'GraphQL', 'Microservices', 'Git', 'GitHub', 'GitLab',
            'Agile', 'Scrum', 'JIRA', 'Confluence'
        ]
        
        text_lower = text.lower()
        for skill in tech_keywords:
            skill_pattern = skill.replace('\\', '')
            if re.search(r'\b' + skill_pattern.lower() + r'\b', text_lower):
                technical_skills.append(skill_pattern)
        
        return technical_skills
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills mentioned in the job description"""
        soft_skills = []
        
        soft_skill_keywords = [
            'communication', 'teamwork', 'leadership', 'problem solving',
            'analytical', 'critical thinking', 'creativity', 'adaptability',
            'time management', 'collaboration', 'interpersonal', 'attention to detail',
            'organizational', 'presentation', 'negotiation', 'conflict resolution'
        ]
        
        text_lower = text.lower()
        for skill in soft_skill_keywords:
            if skill in text_lower:
                soft_skills.append(skill.title())
        
        return soft_skills
    
    def _extract_experience_level(self, text: str) -> str:
        """Extract required years of experience"""
        # Look for patterns like "5+ years", "3-5 years", etc.
        exp_patterns = [
            r'(\d+)\+?\s*years?\s+of\s+experience',
            r'(\d+)\s*to\s*(\d+)\s*years?\s+experience',
            r'minimum\s+(\d+)\s+years?',
            r'at least\s+(\d+)\s+years?'
        ]
        
        text_lower = text.lower()
        for pattern in exp_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(0)
        
        # Check for entry-level, mid-level, senior keywords
        if 'entry level' in text_lower or 'junior' in text_lower:
            return 'Entry Level / Junior'
        elif 'senior' in text_lower or 'lead' in text_lower:
            return 'Senior / Lead'
        elif 'mid level' in text_lower or 'intermediate' in text_lower:
            return 'Mid Level'
        
        return 'Not specified'
    
    def _extract_education_requirements(self, text: str) -> List[str]:
        """Extract education requirements"""
        education = []
        
        education_keywords = [
            r"Bachelor'?s?\s+(?:degree|Degree)?(?:\s+in\s+[\w\s,]+)?",
            r"Master'?s?\s+(?:degree|Degree)?(?:\s+in\s+[\w\s,]+)?",
            r"PhD|Ph\.?D\.?(?:\s+in\s+[\w\s,]+)?",
            r"Associate'?s?\s+(?:degree|Degree)?",
            r"(?:BS|BA|MS|MA|MBA)\s+(?:degree|Degree)?(?:\s+in\s+[\w\s,]+)?"
        ]
        
        for pattern in education_keywords:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend(matches)
        
        return list(set(education))
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        
        # Look for responsibilities section
        resp_match = re.search(
            r'(?i)(responsibilities|duties|role|what you.?ll do)(.*?)(?=(requirements|qualifications|skills|benefits|$))',
            text,
            re.DOTALL
        )
        
        if resp_match:
            resp_text = resp_match.group(2)
            # Extract bullet points or sentences
            bullet_points = re.findall(r'[•\-\*]\s*(.+?)(?=[•\-\*\n]|$)', resp_text)
            if bullet_points:
                responsibilities.extend([point.strip() for point in bullet_points if point.strip()])
            else:
                # Split by sentences if no bullet points
                sentences = re.split(r'[.!?]+', resp_text)
                responsibilities.extend([s.strip() for s in sentences if s.strip() and len(s.strip()) > 20])
        
        return responsibilities
