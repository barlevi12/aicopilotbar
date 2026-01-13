"""Cross-checker for event verification."""

from typing import List, Optional
import logging
from datetime import datetime, timedelta

from ..normalize.schema import RawEvent


logger = logging.getLogger(__name__)


class CrossChecker:
    """Cross-checks events against multiple sources."""
    
    def __init__(self, time_window_hours: int = 24):
        """
        Initialize cross-checker.
        
        Args:
            time_window_hours: Time window for cross-checking related events
        """
        self.time_window = timedelta(hours=time_window_hours)
        self.event_cache = []
    
    def check_event(self, event: RawEvent, all_events: List[RawEvent]) -> tuple[bool, int]:
        """
        Check if an event has confirmation from other sources.
        
        Args:
            event: Event to check
            all_events: List of all collected events
            
        Returns:
            Tuple of (is_cross_checked, num_confirmations)
        """
        confirmations = 0
        
        # Find events with similar content within time window
        for other_event in all_events:
            if other_event.id == event.id:
                continue
            
            # Check time proximity
            time_diff = abs((event.timestamp - other_event.timestamp).total_seconds())
            if time_diff > self.time_window.total_seconds():
                continue
            
            # Check content similarity
            if self._are_similar(event, other_event):
                confirmations += 1
        
        is_cross_checked = confirmations > 0
        return is_cross_checked, confirmations
    
    def _are_similar(self, event1: RawEvent, event2: RawEvent, threshold: float = 0.5) -> bool:
        """
        Check if two events are similar in content.
        
        Args:
            event1: First event
            event2: Second event
            threshold: Similarity threshold (0-1)
            
        Returns:
            True if events are similar
        """
        # Simple keyword-based similarity
        keywords1 = set(self._extract_keywords(event1.headline + " " + event1.content))
        keywords2 = set(self._extract_keywords(event2.headline + " " + event2.content))
        
        if not keywords1 or not keywords2:
            return False
        
        # Jaccard similarity
        intersection = len(keywords1.intersection(keywords2))
        union = len(keywords1.union(keywords2))
        
        similarity = intersection / union if union > 0 else 0
        return similarity >= threshold
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract significant keywords from text.
        
        Args:
            text: Input text
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction (lowercased, length > 3)
        words = text.lower().split()
        stopwords = {'the', 'and', 'for', 'with', 'from', 'this', 'that', 'have', 'has', 'will'}
        keywords = [w for w in words if len(w) > 3 and w not in stopwords]
        return keywords
