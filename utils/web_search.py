"""
Web Search Module
Searches the web for information about skills and technologies.
"""

import os
import re
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchResult:
    """A single search result."""
    title: str
    url: str
    snippet: str
    source: str


class WebSearcher:
    """Search the web for skill/technology information."""

    def __init__(self):
        # DuckDuckGo HTML search (no API key required)
        self.search_url = "https://html.duckduckgo.com/html/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def search(self, query: str, context: str = '') -> list[dict]:
        """
        Search for information about a skill or technology.

        Args:
            query: The search query (skill/technology name)
            context: Additional context for the search

        Returns:
            List of search results with relevant information
        """
        # Enhance query for resume context
        search_query = self._build_search_query(query, context)

        try:
            results = self._perform_search(search_query)
            processed = self._process_results(results, query)
            return processed
        except Exception as e:
            # Return helpful fallback information
            return self._get_fallback_info(query)

    def _build_search_query(self, query: str, context: str) -> str:
        """Build an optimized search query."""
        # Add resume-relevant terms
        resume_terms = "resume example experience description bullet points"

        if context:
            return f"{query} {context} {resume_terms}"
        return f"{query} {resume_terms}"

    def _perform_search(self, query: str) -> list[SearchResult]:
        """Perform the actual web search."""
        results = []

        try:
            # Encode the query
            data = urllib.parse.urlencode({'q': query}).encode('utf-8')

            request = urllib.request.Request(
                self.search_url,
                data=data,
                headers=self.headers,
                method='POST'
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                html = response.read().decode('utf-8')
                results = self._parse_duckduckgo_results(html)

        except Exception:
            # Silent fail, will use fallback
            pass

        return results

    def _parse_duckduckgo_results(self, html: str) -> list[SearchResult]:
        """Parse DuckDuckGo HTML results."""
        results = []

        # Simple regex-based parsing for result links and snippets
        # Pattern for result blocks
        result_pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>'
        snippet_pattern = r'<a class="result__snippet"[^>]*>([^<]+(?:<[^>]+>[^<]*</[^>]+>)*[^<]*)</a>'

        links = re.findall(result_pattern, html)
        snippets = re.findall(snippet_pattern, html)

        for i, (url, title) in enumerate(links[:10]):
            snippet = snippets[i] if i < len(snippets) else ''
            # Clean HTML from snippet
            snippet = re.sub(r'<[^>]+>', '', snippet)

            # Extract actual URL from DuckDuckGo redirect
            if 'uddg=' in url:
                url_match = re.search(r'uddg=([^&]+)', url)
                if url_match:
                    url = urllib.parse.unquote(url_match.group(1))

            results.append(SearchResult(
                title=title.strip(),
                url=url,
                snippet=snippet.strip(),
                source=self._extract_domain(url)
            ))

        return results

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            parsed = urllib.parse.urlparse(url)
            return parsed.netloc
        except Exception:
            return 'unknown'

    def _process_results(self, results: list[SearchResult], query: str) -> list[dict]:
        """Process and enhance search results."""
        processed = []

        for result in results[:5]:  # Limit to top 5
            # Extract actionable content
            bullet_points = self._extract_bullet_points(result.snippet, query)

            processed.append({
                'title': result.title,
                'url': result.url,
                'snippet': result.snippet,
                'source': result.source,
                'suggested_bullets': bullet_points,
                'relevance_score': self._calculate_relevance(result, query)
            })

        # Sort by relevance
        processed.sort(key=lambda x: x['relevance_score'], reverse=True)

        return processed

    def _extract_bullet_points(self, text: str, skill: str) -> list[str]:
        """Extract or generate bullet point suggestions from text."""
        bullets = []

        # Look for action verbs in the text
        action_verbs = [
            'developed', 'implemented', 'designed', 'built', 'created',
            'managed', 'led', 'optimized', 'improved', 'maintained',
            'deployed', 'configured', 'integrated', 'automated',
        ]

        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                sentence_lower = sentence.lower()
                if any(verb in sentence_lower for verb in action_verbs):
                    bullets.append(sentence)
                elif skill.lower() in sentence_lower:
                    bullets.append(sentence)

        return bullets[:3]  # Limit to 3 suggestions

    def _calculate_relevance(self, result: SearchResult, query: str) -> float:
        """Calculate relevance score for a result."""
        score = 0.0
        query_lower = query.lower()

        # Title contains query
        if query_lower in result.title.lower():
            score += 0.4

        # Snippet contains query
        if query_lower in result.snippet.lower():
            score += 0.3

        # Prefer certain sources
        trusted_sources = ['indeed.com', 'linkedin.com', 'glassdoor.com',
                          'resume.io', 'zety.com', 'monster.com']
        if any(source in result.source.lower() for source in trusted_sources):
            score += 0.2

        # Has actionable content
        if result.snippet and len(result.snippet) > 50:
            score += 0.1

        return min(score, 1.0)

    def _get_fallback_info(self, query: str) -> list[dict]:
        """Get fallback information when search fails."""
        # Generate generic but helpful suggestions
        templates = self._get_skill_templates(query)

        return [{
            'title': f'Resume tips for {query}',
            'url': '',
            'snippet': f'Add {query} to your skills section and describe specific projects or tasks where you used it.',
            'source': 'generated',
            'suggested_bullets': templates,
            'relevance_score': 0.5
        }]

    def _get_skill_templates(self, skill: str) -> list[str]:
        """Get template bullet points for common skills."""
        # Generic templates that work for most skills
        templates = [
            f"Utilized {skill} to develop and implement solutions for [project/task]",
            f"Applied {skill} expertise to improve [metric] by [percentage]",
            f"Collaborated with team members using {skill} for [purpose]",
        ]

        # Skill-specific templates
        skill_lower = skill.lower()

        if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'c++', 'go']):
            templates = [
                f"Developed scalable applications using {skill}, improving performance by X%",
                f"Wrote clean, maintainable {skill} code following best practices and design patterns",
                f"Built and deployed {skill}-based microservices handling X requests per second",
            ]
        elif any(db in skill_lower for db in ['sql', 'database', 'mongodb', 'postgresql']):
            templates = [
                f"Designed and optimized {skill} database schemas for high-traffic applications",
                f"Wrote complex {skill} queries reducing data retrieval time by X%",
                f"Implemented {skill} database migrations and maintained data integrity",
            ]
        elif any(cloud in skill_lower for cloud in ['aws', 'azure', 'gcp', 'cloud']):
            templates = [
                f"Architected and deployed cloud infrastructure on {skill}",
                f"Managed {skill} resources reducing infrastructure costs by X%",
                f"Implemented CI/CD pipelines using {skill} services for automated deployments",
            ]
        elif any(soft in skill_lower for soft in ['leadership', 'communication', 'teamwork']):
            templates = [
                f"Demonstrated {skill} by leading cross-functional teams of X members",
                f"Applied {skill} skills to facilitate stakeholder meetings and presentations",
                f"Leveraged {skill} abilities to mentor junior team members",
            ]

        return templates


class ContentGenerator:
    """Generate resume content based on search results."""

    def generate_bullet_point(
        self,
        skill: str,
        context: str,
        project_name: Optional[str] = None
    ) -> str:
        """Generate a resume bullet point for a skill."""
        if project_name:
            return f"Implemented {skill} in {project_name} to {context}"
        return f"Utilized {skill} to {context}"

    def enhance_bullet_point(self, original: str, skill: str) -> str:
        """Enhance an existing bullet point with a skill mention."""
        if skill.lower() not in original.lower():
            # Add skill to the beginning
            return f"Using {skill}, {original[0].lower()}{original[1:]}"
        return original
