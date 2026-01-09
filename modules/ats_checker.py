"""
ATS Checker Module
Evaluates resume ATS compliance and provides optimization suggestions
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class ATSChecker:
    """Check resume for ATS (Applicant Tracking System) compliance"""
    
    def __init__(self):
        """Initialize ATS checker with scoring criteria"""
        # Common ATS-friendly section headers
        self.standard_sections = {
            'experience', 'work experience', 'professional experience', 'employment',
            'education', 'skills', 'technical skills', 'core competencies',
            'summary', 'profile', 'objective', 'certifications', 'projects',
            'achievements', 'accomplishments', 'awards'
        }
        
        # Keywords that indicate poor ATS compatibility
        self.ats_unfriendly_indicators = [
            'table', 'header', 'footer', 'text box', 'image', 'graphic',
            'column', 'watermark'
        ]
        
        # Common professional keywords by category
        self.professional_keywords = {
            'action_verbs': [
                'achieved', 'managed', 'led', 'developed', 'created', 'implemented',
                'designed', 'improved', 'increased', 'reduced', 'analyzed', 'coordinated',
                'executed', 'delivered', 'optimized', 'streamlined', 'established',
                'collaborated', 'initiated', 'transformed', 'spearheaded'
            ],
            'technical': [
                'python', 'java', 'javascript', 'sql', 'aws', 'azure', 'docker',
                'kubernetes', 'git', 'api', 'agile', 'scrum', 'ci/cd', 'linux',
                'react', 'angular', 'node', 'machine learning', 'data analysis'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem-solving',
                'analytical', 'project management', 'strategic planning',
                'decision-making', 'time management', 'adaptability'
            ]
        }
    
    def calculate_ats_score(self, resume_data: Dict, job_requirements: Dict = None) -> Dict:
        """
        Calculate comprehensive ATS compliance score
        
        Args:
            resume_data: Parsed resume data
            job_requirements: Optional job requirements for keyword matching
            
        Returns:
            Dictionary containing score and detailed breakdown
        """
        raw_text = resume_data.get('raw_text', '')
        sections = resume_data.get('sections', [])
        
        # Calculate individual component scores
        format_score = self._check_format_compatibility(raw_text, resume_data)
        structure_score = self._check_structure(sections, raw_text)
        keyword_score = self._check_keywords(raw_text, job_requirements)
        content_score = self._check_content_quality(raw_text)
        
        # Weighted average (format and structure are most important for ATS)
        total_score = (
            format_score['score'] * 0.30 +
            structure_score['score'] * 0.30 +
            keyword_score['score'] * 0.25 +
            content_score['score'] * 0.15
        )
        
        return {
            'total_score': round(total_score, 1),
            'format': format_score,
            'structure': structure_score,
            'keywords': keyword_score,
            'content': content_score,
            'grade': self._get_grade(total_score),
            'recommendations': self._generate_recommendations(
                format_score, structure_score, keyword_score, content_score
            )
        }
    
    def _check_format_compatibility(self, text: str, resume_data: Dict) -> Dict:
        """
        Check if resume format is ATS-friendly
        
        Args:
            text: Resume text content
            resume_data: Parsed resume data
            
        Returns:
            Dictionary with format score and issues
        """
        issues = []
        score = 100.0
        
        # Check for complex formatting indicators
        if len(text) < 100:
            issues.append("Resume appears too short or not properly parsed")
            score -= 30
        
        # Check for unusual characters that might indicate graphics/tables
        special_char_ratio = len(re.findall(r'[^\w\s\-.,;:()@]', text)) / max(len(text), 1)
        if special_char_ratio > 0.05:
            issues.append("Contains many special characters - may have complex formatting")
            score -= 15
        
        # Check text density (should have good spacing)
        lines = text.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        if len(non_empty_lines) < 10:
            issues.append("Very few line breaks - may have formatting issues")
            score -= 10
        
        # Check for bullet points (good for ATS)
        bullet_patterns = len(re.findall(r'[•\-\*]', text))
        if bullet_patterns < 3:
            issues.append("Few or no bullet points detected - use bullets for clarity")
            score -= 10
        
        return {
            'score': max(score, 0),
            'issues': issues,
            'details': f"Format compatibility: {max(score, 0):.1f}%"
        }
    
    def _check_structure(self, sections: List[str], text: str) -> Dict:
        """
        Check resume structure and organization
        
        Args:
            sections: List of identified sections (can be strings or dicts)
            text: Resume text content
            
        Returns:
            Dictionary with structure score and issues
        """
        issues = []
        score = 100.0
        
        # Normalize section names for comparison - handle both strings and dicts
        normalized_sections = set()
        for s in sections:
            if isinstance(s, dict):
                # Extract name from dict
                section_name = s.get('name', '')
                if section_name:
                    normalized_sections.add(section_name.lower().strip())
            elif isinstance(s, str) and s:
                # Use string directly
                normalized_sections.add(s.lower().strip())
        
        # Check for essential sections
        has_experience = any(
            keyword in ' '.join(normalized_sections)
            for keyword in ['experience', 'work', 'employment', 'professional']
        )
        has_education = 'education' in ' '.join(normalized_sections)
        has_skills = any(
            keyword in ' '.join(normalized_sections)
            for keyword in ['skills', 'competencies', 'technologies']
        )
        
        if not has_experience:
            issues.append("Missing clear 'Experience' or 'Work History' section")
            score -= 25
        
        if not has_education:
            issues.append("Missing 'Education' section")
            score -= 20
        
        if not has_skills:
            issues.append("Missing 'Skills' or 'Technical Skills' section")
            score -= 20
        
        # Check section count
        if len(sections) < 3:
            issues.append("Too few sections - add more organized sections")
            score -= 15
        elif len(sections) > 10:
            issues.append("Too many sections - consider consolidating")
            score -= 10
        
        # Check for contact information at the top
        first_200_chars = text[:200].lower()
        has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', first_200_chars))
        has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', first_200_chars))
        
        if not has_email:
            issues.append("Email not found in header - add contact information at top")
            score -= 15
        
        if not has_phone:
            issues.append("Phone number not clearly visible at top")
            score -= 10
        
        return {
            'score': max(score, 0),
            'issues': issues,
            'sections_found': list(normalized_sections),
            'details': f"Structure quality: {max(score, 0):.1f}%"
        }
    
    def _check_keywords(self, text: str, job_requirements: Dict = None) -> Dict:
        """
        Check keyword optimization and density
        
        Args:
            text: Resume text content
            job_requirements: Optional job requirements
            
        Returns:
            Dictionary with keyword score and analysis
        """
        issues = []
        score = 100.0
        text_lower = text.lower()
        
        # Count action verbs
        action_verb_count = sum(
            1 for verb in self.professional_keywords['action_verbs']
            if verb in text_lower
        )
        
        if action_verb_count < 5:
            issues.append("Use more action verbs (achieved, managed, led, etc.)")
            score -= 20
        
        # Count technical keywords
        technical_count = sum(
            1 for keyword in self.professional_keywords['technical']
            if keyword in text_lower
        )
        
        # Count soft skills
        soft_skill_count = sum(
            1 for skill in self.professional_keywords['soft_skills']
            if skill in text_lower
        )
        
        if soft_skill_count < 2:
            issues.append("Include more soft skills (leadership, communication, etc.)")
            score -= 15
        
        # Check keyword density (should be balanced)
        word_count = len(text.split())
        if word_count < 200:
            issues.append("Resume is too short - aim for 400-800 words")
            score -= 25
        elif word_count > 1000:
            issues.append("Resume may be too long - consider condensing to 1-2 pages")
            score -= 10
        
        # Check against job requirements if provided
        job_match_score = 100
        matched_keywords = []
        missing_keywords = []
        
        if job_requirements:
            required_skills = job_requirements.get('technical_skills', []) + \
                            job_requirements.get('soft_skills', [])
            
            if required_skills:
                for skill in required_skills:
                    if skill.lower() in text_lower:
                        matched_keywords.append(skill)
                    else:
                        missing_keywords.append(skill)
                
                match_percentage = len(matched_keywords) / len(required_skills) * 100
                job_match_score = match_percentage
                
                if match_percentage < 50:
                    issues.append(f"Only {match_percentage:.0f}% match with job requirements")
                    score -= 30
                elif match_percentage < 75:
                    issues.append(f"Moderate match ({match_percentage:.0f}%) - add more relevant keywords")
                    score -= 15
        
        return {
            'score': max(score, 0),
            'issues': issues,
            'action_verbs': action_verb_count,
            'technical_keywords': technical_count,
            'soft_skills': soft_skill_count,
            'word_count': word_count,
            'job_match': job_match_score if job_requirements else None,
            'matched_keywords': matched_keywords if job_requirements else [],
            'missing_keywords': missing_keywords if job_requirements else [],
            'details': f"Keyword optimization: {max(score, 0):.1f}%"
        }
    
    def _check_content_quality(self, text: str) -> Dict:
        """
        Check overall content quality
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with content quality score
        """
        issues = []
        score = 100.0
        
        # Check for quantifiable achievements (numbers/metrics)
        numbers_count = len(re.findall(r'\d+%|\$\d+|\d+ (years|months|people|projects|million|thousand)', text.lower()))
        
        if numbers_count < 3:
            issues.append("Add more quantifiable achievements (numbers, percentages, metrics)")
            score -= 20
        
        # Check for common resume mistakes
        if 'references available upon request' in text.lower():
            issues.append("Remove 'References available upon request' - it's outdated")
            score -= 5
        
        if 'curriculum vitae' in text.lower() or text.lower().count('cv') > 2:
            issues.append("Avoid using 'CV' or 'Curriculum Vitae' in US resumes")
            score -= 5
        
        # Check for personal pronouns (should avoid "I", "me", "my")
        pronoun_count = len(re.findall(r'\b(I|me|my)\b', text, re.IGNORECASE))
        if pronoun_count > 5:
            issues.append("Avoid personal pronouns (I, me, my) - use action verbs instead")
            score -= 10
        
        # Check average sentence length (should be concise)
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length > 25:
                issues.append("Sentences are too long - keep them concise and clear")
                score -= 10
        
        return {
            'score': max(score, 0),
            'issues': issues,
            'metrics_count': numbers_count,
            'details': f"Content quality: {max(score, 0):.1f}%"
        }
    
    def _get_grade(self, score: float) -> str:
        """
        Convert numeric score to letter grade
        
        Args:
            score: Numeric score (0-100)
            
        Returns:
            Letter grade
        """
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self, format_score: Dict, structure_score: Dict,
                                  keyword_score: Dict, content_score: Dict) -> List[Dict]:
        """
        Generate prioritized recommendations based on scores
        
        Args:
            format_score: Format compatibility results
            structure_score: Structure quality results
            keyword_score: Keyword optimization results
            content_score: Content quality results
            
        Returns:
            List of recommendations with priority
        """
        recommendations = []
        
        # High priority (critical issues)
        if format_score['score'] < 70:
            recommendations.append({
                'priority': 'high',
                'category': 'Format',
                'message': 'Use a simple, single-column layout without tables or graphics',
                'issues': format_score['issues']
            })
        
        if structure_score['score'] < 70:
            recommendations.append({
                'priority': 'high',
                'category': 'Structure',
                'message': 'Add standard sections (Experience, Education, Skills) with clear headers',
                'issues': structure_score['issues']
            })
        
        # Medium priority
        if keyword_score['score'] < 75:
            recommendations.append({
                'priority': 'medium',
                'category': 'Keywords',
                'message': 'Optimize keyword usage with action verbs and relevant skills',
                'issues': keyword_score['issues']
            })
        
        # Low priority
        if content_score['score'] < 80:
            recommendations.append({
                'priority': 'low',
                'category': 'Content',
                'message': 'Improve content with quantifiable achievements and metrics',
                'issues': content_score['issues']
            })
        
        return recommendations
    
    def generate_optimization_suggestions(self, resume_data: Dict,
                                         job_requirements: Dict = None) -> Dict:
        """
        Generate specific optimization suggestions for improving ATS score
        
        Args:
            resume_data: Parsed resume data
            job_requirements: Optional job requirements
            
        Returns:
            Dictionary with categorized suggestions
        """
        text = resume_data.get('raw_text', '')
        sections = resume_data.get('sections', [])
        
        suggestions = {
            'formatting': [],
            'sections': [],
            'keywords': [],
            'content': []
        }
        
        # Formatting suggestions
        suggestions['formatting'].extend([
            'Use standard fonts: Arial, Calibri, or Times New Roman (10-12pt)',
            'Save as .docx or .pdf format for best compatibility',
            'Use clear section headers in bold or slightly larger font',
            'Maintain consistent spacing between sections',
            'Avoid headers, footers, text boxes, and tables'
        ])
        
        # Section suggestions
        section_lower = set()
        for s in sections:
            if isinstance(s, dict):
                section_name = s.get('name', '')
                if section_name:
                    section_lower.add(section_name.lower())
            elif isinstance(s, str) and s:
                section_lower.add(s.lower())
        
        if not any('experience' in s for s in section_lower):
            suggestions['sections'].append('Add a "Work Experience" or "Professional Experience" section')
        if not any('education' in s for s in section_lower):
            suggestions['sections'].append('Add an "Education" section with degrees and institutions')
        if not any('skill' in s for s in section_lower):
            suggestions['sections'].append('Add a "Skills" section with relevant technical and soft skills')
        
        # Keyword suggestions
        text_lower = text.lower()
        action_verbs_missing = [
            verb for verb in self.professional_keywords['action_verbs'][:10]
            if verb not in text_lower
        ]
        if action_verbs_missing:
            suggestions['keywords'].append(
                f'Consider adding action verbs: {", ".join(action_verbs_missing[:5])}'
            )
        
        # Job-specific keyword suggestions
        if job_requirements:
            missing_skills = []
            for skill in job_requirements.get('technical_skills', [])[:10]:
                if skill.lower() not in text_lower:
                    missing_skills.append(skill)
            
            if missing_skills:
                suggestions['keywords'].append(
                    f'Add job-specific keywords: {", ".join(missing_skills[:5])}'
                )
        
        # Content suggestions
        suggestions['content'].extend([
            'Use bullet points to list accomplishments and responsibilities',
            'Include quantifiable achievements (numbers, percentages, dollar amounts)',
            'Start bullet points with strong action verbs',
            'Keep descriptions concise (1-2 lines per bullet)',
            'Remove personal pronouns (I, me, my)',
            'Focus on results and impact rather than just duties'
        ])
        
        return suggestions
