"""
Web Search Engine Module
Searches the internet for information about missing points
"""

import json
import re
from typing import Dict, List


class WebSearchEngine:
    """Search the web for information about skills and responsibilities"""
    
    def __init__(self):
        self.search_templates = {
            'technical_skill': '{skill} examples in resume',
            'soft_skill': 'how to demonstrate {skill} in resume',
            'responsibility': '{responsibility} resume bullet points',
            'experience': 'resume examples for {experience}'
        }
    
    def search(self, query: str, search_type: str = 'general') -> List[Dict]:
        """
        Search for information about a specific point
        
        Args:
            query: The search query
            search_type: Type of search (technical_skill, soft_skill, etc.)
            
        Returns:
            List of search results with suggestions
        """
        # In a real implementation, this would use a search API like Google Custom Search,
        # Bing API, or DuckDuckGo. For now, we'll provide template suggestions.
        
        suggestions = self._generate_suggestions(query, search_type)
        
        return suggestions
    
    def _generate_suggestions(self, query: str, search_type: str) -> List[Dict]:
        """Generate helpful suggestions based on the query"""
        suggestions = []
        
        # Clean the query
        query_clean = query.strip()
        
        # Generate context-aware suggestions
        if self._is_technical_skill(query_clean):
            suggestions.extend(self._get_technical_skill_suggestions(query_clean))
        elif self._is_soft_skill(query_clean):
            suggestions.extend(self._get_soft_skill_suggestions(query_clean))
        else:
            suggestions.extend(self._get_general_suggestions(query_clean))
        
        return suggestions
    
    def _is_technical_skill(self, text: str) -> bool:
        """Check if text represents a technical skill"""
        tech_indicators = [
            'python', 'java', 'javascript', 'react', 'angular', 'node',
            'sql', 'database', 'cloud', 'aws', 'azure', 'docker', 'kubernetes',
            'api', 'framework', 'library', 'programming', 'development'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in tech_indicators)
    
    def _is_soft_skill(self, text: str) -> bool:
        """Check if text represents a soft skill"""
        soft_indicators = [
            'communication', 'leadership', 'teamwork', 'collaboration',
            'problem solving', 'analytical', 'management', 'organizational'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in soft_indicators)
    
    def _get_technical_skill_suggestions(self, skill: str) -> List[Dict]:
        """Get suggestions for technical skills"""
        return [
            {
                'title': f'Example 1: Project Implementation',
                'content': f'Developed and deployed {skill}-based application with X features, resulting in Y% improvement in performance',
                'source': 'Resume Best Practices'
            },
            {
                'title': f'Example 2: Technical Leadership',
                'content': f'Led technical initiative using {skill} to optimize system architecture, reducing processing time by X%',
                'source': 'Resume Best Practices'
            },
            {
                'title': f'Example 3: Problem Solving',
                'content': f'Utilized {skill} to solve critical production issues, improving system reliability by X%',
                'source': 'Resume Best Practices'
            },
            {
                'title': f'Example 4: Collaboration',
                'content': f'Collaborated with cross-functional teams to implement {skill} solutions, delivering project X weeks ahead of schedule',
                'source': 'Resume Best Practices'
            }
        ]
    
    def _get_soft_skill_suggestions(self, skill: str) -> List[Dict]:
        """Get suggestions for soft skills"""
        examples = {
            'communication': [
                'Presented technical findings to stakeholders, facilitating data-driven decision making',
                'Authored comprehensive documentation resulting in 30% reduction in onboarding time',
                'Conducted weekly team meetings to align on project goals and deliverables'
            ],
            'leadership': [
                'Led team of X engineers in developing critical system features',
                'Mentored junior developers, improving team productivity by X%',
                'Spearheaded initiative that resulted in Y outcome'
            ],
            'teamwork': [
                'Collaborated with cross-functional teams across X departments',
                'Participated in agile ceremonies and contributed to sprint planning',
                'Worked closely with designers and product managers to deliver user-centric solutions'
            ],
            'problem solving': [
                'Identified and resolved critical system bottleneck, improving performance by X%',
                'Developed innovative solution to reduce processing time from X to Y',
                'Analyzed complex issues and implemented effective solutions'
            ]
        }
        
        skill_lower = skill.lower()
        matching_examples = []
        
        for key, examples_list in examples.items():
            if key in skill_lower:
                matching_examples = examples_list
                break
        
        if not matching_examples:
            matching_examples = [
                f'Demonstrated {skill} by achieving measurable results',
                f'Applied {skill} in collaborative team environment',
                f'Utilized {skill} to drive project success'
            ]
        
        return [
            {
                'title': f'Example {i+1}',
                'content': example,
                'source': 'Resume Best Practices'
            }
            for i, example in enumerate(matching_examples)
        ]
    
    def _get_general_suggestions(self, query: str) -> List[Dict]:
        """Get general suggestions for any query"""
        return [
            {
                'title': 'Action-Oriented Example',
                'content': f'Accomplished [X] as measured by [Y] by doing [Z] related to: {query}',
                'source': 'Resume Best Practices'
            },
            {
                'title': 'Results-Focused Example',
                'content': f'Improved/Increased/Reduced [metric] by X% through [action] involving: {query}',
                'source': 'Resume Best Practices'
            },
            {
                'title': 'Leadership Example',
                'content': f'Led/Managed/Coordinated [team/project] to achieve [outcome] using: {query}',
                'source': 'Resume Best Practices'
            },
            {
                'title': 'Technical Example',
                'content': f'Developed/Implemented/Designed [solution] resulting in [benefit] related to: {query}',
                'source': 'Resume Best Practices'
            }
        ]
    
    def format_for_resume(self, suggestion: str, context: Dict = None) -> str:
        """
        Format a suggestion to be resume-ready
        
        Args:
            suggestion: The suggestion text
            context: Additional context (project name, metrics, etc.)
            
        Returns:
            Formatted resume bullet point
        """
        # Ensure it starts with an action verb
        action_verbs = [
            'Developed', 'Implemented', 'Designed', 'Created', 'Built',
            'Led', 'Managed', 'Coordinated', 'Directed', 'Supervised',
            'Improved', 'Increased', 'Reduced', 'Optimized', 'Enhanced',
            'Collaborated', 'Partnered', 'Worked', 'Contributed', 'Participated',
            'Analyzed', 'Researched', 'Investigated', 'Evaluated', 'Assessed'
        ]
        
        suggestion = suggestion.strip()
        
        # Check if it already starts with an action verb
        starts_with_verb = any(suggestion.startswith(verb) for verb in action_verbs)
        
        if not starts_with_verb and context:
            # Prepend an appropriate action verb
            suggestion = f"Developed {suggestion}"
        
        # Ensure it's concise (under 150 characters ideally)
        if len(suggestion) > 150:
            suggestion = suggestion[:147] + '...'
        
        return suggestion
