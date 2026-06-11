"""Text processing utilities for AI Organization OS"""

import re
from typing import List

def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and formatting.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs.
    
    Args:
        text: Text to split
        
    Returns:
        List of paragraphs
    """
    # Split by double newlines
    paragraphs = text.split('\n\n')
    
    # Filter empty paragraphs and clean
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    return paragraphs

def extract_sections(text: str) -> dict:
    """
    Extract numbered or bulleted sections from text.
    
    Args:
        text: Text containing sections
        
    Returns:
        Dictionary of sections
    """
    sections = {}
    
    # Find headings (lines that start with numbers, bullets, or caps)
    lines = text.split('\n')
    current_section = "intro"
    current_content = []
    
    for line in lines:
        if re.match(r'^[\d]+\.|^[-*•]|^[A-Z][A-Z]+', line):
            if current_content:
                sections[current_section] = '\n'.join(current_content).strip()
                current_content = []
            
            current_section = line[:50].strip()
        else:
            current_content.append(line)
    
    if current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def count_tokens_approx(text: str) -> int:
    """
    Approximate token count (rough estimate).
    
    Args:
        text: Text to count
        
    Returns:
        Approximate token count
    """
    # Rough approximation: ~4 chars per token
    return len(text) // 4

def format_for_display(text: str, max_chars: int = 2000) -> str:
    """
    Format text for display (truncate if needed).
    
    Args:
        text: Text to format
        max_chars: Maximum characters to display
        
    Returns:
        Formatted text
    """
    if len(text) > max_chars:
        return truncate_text(text, max_chars)
    
    return text

def highlight_key_phrases(text: str, phrases: List[str]) -> str:
    """
    Highlight key phrases in text (for HTML output).
    
    Args:
        text: Text to highlight
        phrases: List of phrases to highlight
        
    Returns:
        Text with HTML highlights
    """
    result = text
    
    for phrase in phrases:
        # Case-insensitive highlighting
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        result = pattern.sub(f'<mark>{phrase}</mark>', result)
    
    return result
