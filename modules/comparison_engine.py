"""
Comparison Engine Module
Compares resume with job requirements to find missing points
"""

from typing import Dict, List, Set


class ComparisonEngine:
    """Compare resume data with job requirements"""
    
    def __init__(self):
        pass
    
    def find_missing_points(self, resume_data: Dict, job_requirements: Dict) -> List[Dict]:
        """
        Compare resume with job requirements and identify missing points
        
        Args:
            resume_data: Parsed resume data
            job_requirements: Analyzed job requirements
            
        Returns:
            List of missing points with details
        """
        missing_points = []
        
        # Compare technical skills
        missing_skills = self._find_missing_skills(
            resume_data.get('skills', []),
            job_requirements.get('technical_skills', [])
        )
        
        for skill in missing_skills:
            missing_points.append({
                'type': 'technical_skill',
                'content': skill,
                'priority': 'high',
                'description': f'Technical skill: {skill}'
            })
        
        # Compare soft skills
        resume_text = resume_data.get('raw_text', '').lower()
        for soft_skill in job_requirements.get('soft_skills', []):
            if soft_skill.lower() not in resume_text:
                missing_points.append({
                    'type': 'soft_skill',
                    'content': soft_skill,
                    'priority': 'medium',
                    'description': f'Soft skill: {soft_skill}'
                })
        
        # Check responsibilities alignment
        responsibilities = job_requirements.get('responsibilities', [])
        for responsibility in responsibilities[:5]:  # Limit to top 5
            if not self._check_responsibility_coverage(responsibility, resume_text):
                missing_points.append({
                    'type': 'responsibility',
                    'content': responsibility,
                    'priority': 'high',
                    'description': f'Responsibility: {responsibility}'
                })
        
        # Check education requirements
        resume_education_text = ' '.join([e.get('text', '') for e in resume_data.get('education', [])])
        for edu_req in job_requirements.get('education', []):
            if not self._check_education_match(edu_req, resume_education_text):
                missing_points.append({
                    'type': 'education',
                    'content': edu_req,
                    'priority': 'medium',
                    'description': f'Education requirement: {edu_req}'
                })
        
        # Check experience level
        exp_level = job_requirements.get('experience_level', '')
        if exp_level and exp_level != 'Not specified':
            if not self._check_experience_match(exp_level, resume_text):
                missing_points.append({
                    'type': 'experience',
                    'content': exp_level,
                    'priority': 'high',
                    'description': f'Experience requirement: {exp_level}'
                })
        
        return missing_points
    
    def _find_missing_skills(self, resume_skills: List[str], required_skills: List[str]) -> List[str]:
        """Find skills that are in requirements but not in resume"""
        resume_skills_set = set([skill.lower() for skill in resume_skills])
        required_skills_set = set([skill.lower() for skill in required_skills])
        
        missing = required_skills_set - resume_skills_set
        
        # Return original case versions
        return [skill for skill in required_skills if skill.lower() in missing]
    
    def _check_responsibility_coverage(self, responsibility: str, resume_text: str) -> bool:
        """Check if a responsibility is covered in the resume"""
        # Extract key words from responsibility
        key_words = self._extract_keywords(responsibility)
        
        # Check if at least 50% of keywords are in resume
        matches = sum(1 for word in key_words if word.lower() in resume_text)
        
        return matches >= len(key_words) * 0.5 if key_words else False
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Remove common words
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'we', 'you', 'they', 'it', 'our', 'your'
        }
        
        words = text.lower().split()
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        
        return keywords
    
    def _check_education_match(self, requirement: str, education_text: str) -> bool:
        """Check if education requirement is met"""
        req_lower = requirement.lower()
        edu_lower = education_text.lower()
        
        # Extract degree type
        if 'bachelor' in req_lower or 'bs' in req_lower or 'ba' in req_lower:
            return 'bachelor' in edu_lower or 'bs' in edu_lower or 'ba' in edu_lower or \
                   'master' in edu_lower or 'ms' in edu_lower or 'phd' in edu_lower
        elif 'master' in req_lower or 'ms' in req_lower or 'ma' in req_lower:
            return 'master' in edu_lower or 'ms' in edu_lower or 'ma' in edu_lower or \
                   'phd' in edu_lower
        elif 'phd' in req_lower or 'ph.d' in req_lower:
            return 'phd' in edu_lower or 'ph.d' in edu_lower
        
        return False
    
    def _check_experience_match(self, requirement: str, resume_text: str) -> bool:
        """Check if experience requirement is mentioned"""
        # Extract years from requirement
        import re
        years_match = re.search(r'(\d+)', requirement)
        
        if years_match:
            required_years = int(years_match.group(1))
            # Check if resume mentions similar or higher years
            resume_years = re.findall(r'(\d+)\+?\s*years?', resume_text.lower())
            
            if resume_years:
                max_years = max([int(y) for y in resume_years])
                return max_years >= required_years
        
        return False
