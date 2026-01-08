"""
Resume Analyzer Module
Compares resume content against job requirements to identify gaps.
"""

import re
from dataclasses import dataclass, field
from difflib import SequenceMatcher


@dataclass
class AnalysisResult:
    """Results of resume analysis against job requirements."""
    match_score: float = 0.0
    matched_points: list[dict] = field(default_factory=list)
    missing_points: list[dict] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'match_score': self.match_score,
            'matched_points': self.matched_points,
            'missing_points': self.missing_points,
            'suggestions': self.suggestions
        }


class ResumeAnalyzer:
    """Analyze resume against job requirements."""

    def __init__(self, similarity_threshold: float = 0.6):
        self.similarity_threshold = similarity_threshold

    def analyze(
        self,
        resume_text: str,
        resume_sections: dict,
        job_requirements: dict
    ) -> dict:
        """
        Analyze resume against job requirements.

        Args:
            resume_text: Full text of resume
            resume_sections: Dictionary of resume sections
            job_requirements: Dictionary of job requirements

        Returns:
            Analysis result dictionary
        """
        result = AnalysisResult()
        resume_text_lower = resume_text.lower()

        all_requirements = self._collect_requirements(job_requirements)
        total_requirements = len(all_requirements)

        if total_requirements == 0:
            result.match_score = 100.0
            return result.to_dict()

        matched_count = 0

        for req in all_requirements:
            keyword = req['keyword']
            category = req['category']
            importance = req.get('importance', 'required')

            # Check if requirement is in resume
            match_info = self._check_match(keyword, resume_text_lower, resume_sections)

            if match_info['matched']:
                matched_count += 1
                result.matched_points.append({
                    'keyword': keyword,
                    'category': category,
                    'importance': importance,
                    'found_in': match_info['found_in'],
                    'context': match_info['context']
                })
            else:
                # Find similar terms that might be present
                similar = self._find_similar_terms(keyword, resume_text_lower)

                result.missing_points.append({
                    'keyword': keyword,
                    'category': category,
                    'importance': importance,
                    'similar_found': similar,
                    'suggested_sections': self._suggest_sections(category),
                    'search_query': self._generate_search_query(keyword, category)
                })

        # Calculate match score
        result.match_score = round((matched_count / total_requirements) * 100, 1)

        # Generate suggestions
        result.suggestions = self._generate_suggestions(result)

        return result.to_dict()

    def _collect_requirements(self, job_requirements: dict) -> list[dict]:
        """Collect all requirements into a flat list with metadata."""
        requirements = []

        # Technologies
        for tech in job_requirements.get('technologies', []):
            requirements.append({
                'keyword': tech,
                'category': 'technology',
                'importance': 'required'
            })

        # Required skills
        for skill in job_requirements.get('required_skills', []):
            if skill not in [r['keyword'] for r in requirements]:
                requirements.append({
                    'keyword': skill,
                    'category': 'skill',
                    'importance': 'required'
                })

        # Preferred skills
        for skill in job_requirements.get('preferred_skills', []):
            if skill not in [r['keyword'] for r in requirements]:
                requirements.append({
                    'keyword': skill,
                    'category': 'skill',
                    'importance': 'preferred'
                })

        # Soft skills
        for skill in job_requirements.get('soft_skills', []):
            requirements.append({
                'keyword': skill,
                'category': 'soft_skill',
                'importance': 'required'
            })

        # Certifications
        for cert in job_requirements.get('certifications', []):
            requirements.append({
                'keyword': cert,
                'category': 'certification',
                'importance': 'preferred'
            })

        # Experience requirements
        for exp in job_requirements.get('experience_requirements', []):
            requirements.append({
                'keyword': exp,
                'category': 'experience',
                'importance': 'required'
            })

        # Keywords
        for kw in job_requirements.get('keywords', []):
            if kw not in [r['keyword'] for r in requirements]:
                requirements.append({
                    'keyword': kw,
                    'category': 'keyword',
                    'importance': 'preferred'
                })

        return requirements

    def _check_match(
        self,
        keyword: str,
        resume_text_lower: str,
        resume_sections: dict
    ) -> dict:
        """Check if a keyword/requirement is present in resume."""
        keyword_lower = keyword.lower()

        # Direct match
        if keyword_lower in resume_text_lower:
            # Find which section contains it
            found_in = []
            for section_name, section_content in resume_sections.items():
                if keyword_lower in section_content.lower():
                    found_in.append(section_name)

            # Extract context (surrounding text)
            context = self._extract_context(keyword_lower, resume_text_lower)

            return {
                'matched': True,
                'found_in': found_in if found_in else ['general'],
                'context': context
            }

        # Check for variations
        variations = self._get_keyword_variations(keyword)
        for var in variations:
            if var.lower() in resume_text_lower:
                found_in = []
                for section_name, section_content in resume_sections.items():
                    if var.lower() in section_content.lower():
                        found_in.append(section_name)

                context = self._extract_context(var.lower(), resume_text_lower)

                return {
                    'matched': True,
                    'found_in': found_in if found_in else ['general'],
                    'context': context
                }

        return {'matched': False, 'found_in': [], 'context': ''}

    def _get_keyword_variations(self, keyword: str) -> list[str]:
        """Get common variations of a keyword."""
        variations = []

        # Handle common abbreviations and full forms
        abbrev_map = {
            'javascript': ['js', 'javascript', 'ecmascript'],
            'typescript': ['ts', 'typescript'],
            'python': ['python', 'py'],
            'kubernetes': ['kubernetes', 'k8s', 'kube'],
            'postgresql': ['postgresql', 'postgres', 'psql'],
            'mongodb': ['mongodb', 'mongo'],
            'continuous integration': ['ci', 'ci/cd', 'continuous integration'],
            'continuous deployment': ['cd', 'ci/cd', 'continuous deployment'],
            'amazon web services': ['aws', 'amazon web services'],
            'google cloud platform': ['gcp', 'google cloud', 'google cloud platform'],
            'machine learning': ['ml', 'machine learning'],
            'artificial intelligence': ['ai', 'artificial intelligence'],
            'natural language processing': ['nlp', 'natural language processing'],
            'restful': ['rest', 'restful', 'rest api'],
        }

        keyword_lower = keyword.lower()
        for full_form, abbrevs in abbrev_map.items():
            if keyword_lower in abbrevs:
                variations.extend(abbrevs)

        # Handle hyphenation variations
        if '-' in keyword:
            variations.append(keyword.replace('-', ' '))
            variations.append(keyword.replace('-', ''))
        else:
            variations.append(keyword.replace(' ', '-'))

        # Handle .js/.py extensions
        if keyword_lower.endswith('.js'):
            variations.append(keyword_lower[:-3])
        elif keyword_lower.endswith('.py'):
            variations.append(keyword_lower[:-3])

        return list(set(variations))

    def _extract_context(self, keyword: str, text: str, context_chars: int = 100) -> str:
        """Extract surrounding context for a keyword match."""
        pos = text.find(keyword)
        if pos == -1:
            return ''

        start = max(0, pos - context_chars)
        end = min(len(text), pos + len(keyword) + context_chars)

        context = text[start:end]

        # Clean up context
        if start > 0:
            context = '...' + context
        if end < len(text):
            context = context + '...'

        return context.strip()

    def _find_similar_terms(self, keyword: str, resume_text: str) -> list[str]:
        """Find similar terms in resume that might be related."""
        similar = []
        keyword_lower = keyword.lower()

        # Split resume into words
        words = re.findall(r'\b\w+\b', resume_text)
        unique_words = set(words)

        for word in unique_words:
            if len(word) > 3:  # Skip short words
                similarity = SequenceMatcher(None, keyword_lower, word).ratio()
                if similarity > self.similarity_threshold:
                    similar.append(word)

        return similar[:5]  # Return top 5

    def _suggest_sections(self, category: str) -> list[str]:
        """Suggest which resume sections a requirement could be added to."""
        section_map = {
            'technology': ['skills', 'projects', 'experience'],
            'skill': ['skills', 'summary', 'experience'],
            'soft_skill': ['summary', 'experience', 'achievements'],
            'certification': ['certifications', 'education'],
            'experience': ['experience', 'summary'],
            'keyword': ['skills', 'summary', 'experience', 'projects'],
        }

        return section_map.get(category, ['experience', 'skills'])

    def _generate_search_query(self, keyword: str, category: str) -> str:
        """Generate a search query to find information about a requirement."""
        if category == 'technology':
            return f"{keyword} resume examples experience description"
        elif category == 'certification':
            return f"{keyword} certification requirements how to get"
        elif category == 'soft_skill':
            return f"{keyword} examples resume how to demonstrate"
        else:
            return f"{keyword} resume description examples"

    def _generate_suggestions(self, result: AnalysisResult) -> list[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []

        # Count missing by importance
        required_missing = [p for p in result.missing_points if p['importance'] == 'required']
        preferred_missing = [p for p in result.missing_points if p['importance'] == 'preferred']

        if required_missing:
            tech_missing = [p for p in required_missing if p['category'] == 'technology']
            if tech_missing:
                tech_names = [p['keyword'] for p in tech_missing[:5]]
                suggestions.append(
                    f"Add these key technologies to your skills/experience: {', '.join(tech_names)}"
                )

        if result.match_score < 50:
            suggestions.append(
                "Your resume matches less than 50% of requirements. "
                "Consider tailoring it specifically for this role."
            )

        # Suggest sections to enhance
        sections_to_enhance = set()
        for point in result.missing_points[:10]:
            sections_to_enhance.update(point['suggested_sections'])

        if sections_to_enhance:
            suggestions.append(
                f"Focus on enhancing these sections: {', '.join(sections_to_enhance)}"
            )

        return suggestions


def calculate_keyword_density(text: str, keyword: str) -> float:
    """Calculate how often a keyword appears per 100 words."""
    words = text.split()
    if not words:
        return 0.0

    keyword_lower = keyword.lower()
    count = sum(1 for word in words if keyword_lower in word.lower())

    return (count / len(words)) * 100
