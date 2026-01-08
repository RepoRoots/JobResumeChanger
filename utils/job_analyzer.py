"""
Job Description Analyzer Module
Extracts key requirements, skills, and qualifications from job descriptions.
"""

import re
from dataclasses import dataclass, field


@dataclass
class JobRequirements:
    """Structured representation of job requirements."""
    required_skills: list[str] = field(default_factory=list)
    preferred_skills: list[str] = field(default_factory=list)
    experience_requirements: list[str] = field(default_factory=list)
    education_requirements: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    soft_skills: list[str] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    responsibilities: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'required_skills': self.required_skills,
            'preferred_skills': self.preferred_skills,
            'experience_requirements': self.experience_requirements,
            'education_requirements': self.education_requirements,
            'certifications': self.certifications,
            'soft_skills': self.soft_skills,
            'technologies': self.technologies,
            'responsibilities': self.responsibilities,
            'keywords': self.keywords
        }


class JobAnalyzer:
    """Analyze job descriptions to extract requirements."""

    # Common technology keywords
    TECH_KEYWORDS = {
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go',
        'golang', 'rust', 'scala', 'kotlin', 'swift', 'php', 'perl', 'r',
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'nodejs', 'express',
        'django', 'flask', 'fastapi', 'spring', 'spring boot', '.net', 'asp.net',
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'cassandra', 'dynamodb', 'oracle', 'sql server', 'sqlite',
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s',
        'jenkins', 'ci/cd', 'terraform', 'ansible', 'chef', 'puppet',
        # Data & ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
        'pandas', 'numpy', 'scikit-learn', 'spark', 'hadoop', 'kafka',
        # Tools & Frameworks
        'git', 'github', 'gitlab', 'jira', 'confluence', 'agile', 'scrum',
        'rest', 'restful', 'api', 'graphql', 'microservices', 'linux', 'unix',
    }

    # Soft skills keywords
    SOFT_SKILLS = {
        'communication', 'leadership', 'teamwork', 'problem-solving',
        'problem solving', 'analytical', 'critical thinking', 'creativity',
        'adaptability', 'time management', 'attention to detail',
        'collaboration', 'interpersonal', 'presentation', 'negotiation',
        'decision-making', 'decision making', 'conflict resolution',
        'self-motivated', 'proactive', 'initiative', 'mentoring',
    }

    # Certification keywords
    CERT_KEYWORDS = {
        'certified', 'certification', 'certificate', 'license', 'licensed',
        'aws certified', 'azure certified', 'gcp certified', 'pmp', 'scrum master',
        'csm', 'cissp', 'cisa', 'cism', 'comptia', 'ccna', 'ccnp', 'cka',
    }

    def __init__(self):
        self.tech_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(t) for t in self.TECH_KEYWORDS) + r')\b',
            re.IGNORECASE
        )

    def analyze(self, job_description: str) -> dict:
        """
        Analyze a job description and extract requirements.

        Args:
            job_description: The job description text

        Returns:
            Dictionary containing categorized requirements
        """
        requirements = JobRequirements()

        # Clean and normalize text
        text = self._clean_text(job_description)

        # Extract different requirement types
        requirements.technologies = self._extract_technologies(text)
        requirements.soft_skills = self._extract_soft_skills(text)
        requirements.certifications = self._extract_certifications(text)
        requirements.experience_requirements = self._extract_experience(text)
        requirements.education_requirements = self._extract_education(text)
        requirements.responsibilities = self._extract_responsibilities(text)

        # Categorize skills into required vs preferred
        required, preferred = self._categorize_skills(text)
        requirements.required_skills = required
        requirements.preferred_skills = preferred

        # Extract additional keywords
        requirements.keywords = self._extract_keywords(text)

        return requirements.to_dict()

    def _clean_text(self, text: str) -> str:
        """Clean and normalize job description text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize bullet points
        text = re.sub(r'[•●◦○▪▫]', '- ', text)
        return text.strip()

    def _extract_technologies(self, text: str) -> list[str]:
        """Extract technology keywords from text."""
        found = set()
        text_lower = text.lower()

        for tech in self.TECH_KEYWORDS:
            # Use word boundary matching
            pattern = r'\b' + re.escape(tech) + r'\b'
            if re.search(pattern, text_lower):
                found.add(tech.title() if len(tech) > 3 else tech.upper())

        return sorted(list(found))

    def _extract_soft_skills(self, text: str) -> list[str]:
        """Extract soft skills from text."""
        found = set()
        text_lower = text.lower()

        for skill in self.SOFT_SKILLS:
            if skill in text_lower:
                found.add(skill.title())

        return sorted(list(found))

    def _extract_certifications(self, text: str) -> list[str]:
        """Extract certification requirements."""
        certs = []
        text_lower = text.lower()

        # Look for specific certification mentions
        cert_patterns = [
            r'(?:aws|amazon)\s+certified\s+[\w\s-]+',
            r'(?:azure|microsoft)\s+certified\s+[\w\s-]+',
            r'(?:google|gcp)\s+certified\s+[\w\s-]+',
            r'pmp\s+(?:certification|certified)?',
            r'scrum\s+master\s+(?:certification|certified)?',
            r'cissp',
            r'comptia\s+[\w+]+',
            r'(?:ccna|ccnp|ccie)',
            r'cka|ckad',
        ]

        for pattern in cert_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                certs.append(match.strip().title())

        return list(set(certs))

    def _extract_experience(self, text: str) -> list[str]:
        """Extract experience requirements."""
        experience = []

        # Pattern for years of experience
        exp_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)',
            r'(?:minimum|at least|min)\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience)?',
        ]

        for pattern in exp_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                experience.append(match.group(0).strip())

        # Look for experience with specific technologies
        tech_exp_pattern = r'experience\s+(?:with|in|using)\s+([^.;,]+)'
        matches = re.finditer(tech_exp_pattern, text, re.IGNORECASE)
        for match in matches:
            exp_text = match.group(1).strip()
            if len(exp_text) < 100:  # Avoid capturing too much text
                experience.append(f"Experience with {exp_text}")

        return list(set(experience))

    def _extract_education(self, text: str) -> list[str]:
        """Extract education requirements."""
        education = []

        edu_patterns = [
            r"(?:bachelor'?s?|master'?s?|phd|doctorate|associate'?s?)\s+(?:degree\s+)?(?:in\s+)?[\w\s]+",
            r'(?:bs|ba|ms|ma|mba|phd)\s+(?:in\s+)?[\w\s]+',
            r'(?:computer science|engineering|mathematics|physics|business)',
        ]

        for pattern in edu_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                clean = match.strip()
                if len(clean) < 100:
                    education.append(clean.title())

        return list(set(education))

    def _extract_responsibilities(self, text: str) -> list[str]:
        """Extract key responsibilities from job description."""
        responsibilities = []

        # Split by common delimiters
        lines = re.split(r'[•●\n]', text)

        # Keywords that indicate responsibilities
        resp_indicators = [
            'develop', 'design', 'implement', 'build', 'create', 'maintain',
            'manage', 'lead', 'collaborate', 'analyze', 'review', 'test',
            'deploy', 'monitor', 'optimize', 'troubleshoot', 'support',
            'document', 'architect', 'integrate', 'automate',
        ]

        for line in lines:
            line = line.strip()
            if len(line) > 20 and len(line) < 300:
                line_lower = line.lower()
                if any(ind in line_lower for ind in resp_indicators):
                    responsibilities.append(line)

        return responsibilities[:15]  # Limit to top 15

    def _categorize_skills(self, text: str) -> tuple[list[str], list[str]]:
        """Categorize skills into required and preferred."""
        required = []
        preferred = []

        text_lower = text.lower()

        # Find required skills section
        required_patterns = [
            r'(?:required|must have|essential|mandatory)[:\s]+([^.]+)',
            r'(?:requirements|qualifications)[:\s]+([^.]+)',
        ]

        # Find preferred skills section
        preferred_patterns = [
            r'(?:preferred|nice to have|bonus|plus|desired)[:\s]+([^.]+)',
            r'(?:preferred qualifications)[:\s]+([^.]+)',
        ]

        # Extract from required sections
        for pattern in required_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                skills_text = match.group(1)
                found_techs = self._extract_technologies(skills_text)
                required.extend(found_techs)

        # Extract from preferred sections
        for pattern in preferred_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                skills_text = match.group(1)
                found_techs = self._extract_technologies(skills_text)
                preferred.extend(found_techs)

        # Remove duplicates
        required = list(set(required))
        preferred = list(set(p for p in preferred if p not in required))

        return required, preferred

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract important keywords from job description."""
        keywords = set()

        # Add all found technologies
        keywords.update(self._extract_technologies(text))

        # Add soft skills
        keywords.update(self._extract_soft_skills(text))

        # Extract action verbs and industry terms
        important_terms = [
            'agile', 'scrum', 'kanban', 'waterfall',
            'full-stack', 'frontend', 'backend', 'devops',
            'data engineering', 'data science', 'machine learning',
            'artificial intelligence', 'cloud computing',
            'distributed systems', 'microservices', 'api design',
            'system design', 'architecture', 'security',
            'performance optimization', 'scalability',
        ]

        text_lower = text.lower()
        for term in important_terms:
            if term in text_lower:
                keywords.add(term.title())

        return sorted(list(keywords))
