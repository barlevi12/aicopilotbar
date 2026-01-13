"""Event deduplicator."""

from typing import List, Set
import logging
from datetime import timedelta

from ..normalize.schema import NormalizedEvent


logger = logging.getLogger(__name__)


class Deduplicator:
    """Removes duplicate events based on similarity."""
    
    def __init__(self, similarity_threshold: float = 0.85, time_window_hours: int = 24):
        """
        Initialize deduplicator.
        
        Args:
            similarity_threshold: Threshold for considering events as duplicates (0-1)
            time_window_hours: Time window for duplicate detection
        """
        self.similarity_threshold = similarity_threshold
        self.time_window = timedelta(hours=time_window_hours)
    
    def dedupe(self, events: List[NormalizedEvent]) -> List[NormalizedEvent]:
        """
        Remove duplicate events.
        
        Args:
            events: List of events to deduplicate
            
        Returns:
            List of unique events
        """
        if not events:
            return []
        
        # Sort by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        
        unique_events = []
        seen_ids: Set[str] = set()
        
        for event in sorted_events:
            if event.id in seen_ids:
                continue
            
            # Check if this event is a duplicate of any kept event
            is_duplicate = False
            for kept_event in unique_events:
                # Check time proximity
                time_diff = abs((event.timestamp - kept_event.timestamp).total_seconds())
                if time_diff > self.time_window.total_seconds():
                    continue
                
                # Check similarity
                if self._are_similar(event, kept_event):
                    is_duplicate = True
                    logger.debug(f"Event {event.id} is duplicate of {kept_event.id}")
                    break
            
            if not is_duplicate:
                unique_events.append(event)
                seen_ids.add(event.id)
        
        logger.info(f"Deduplicated {len(events)} events to {len(unique_events)} unique events")
        return unique_events
    
    def _are_similar(self, event1: NormalizedEvent, event2: NormalizedEvent) -> bool:
        """
        Check if two events are similar enough to be considered duplicates.
        
        Args:
            event1: First event
            event2: Second event
            
        Returns:
            True if events are similar
        """
        # Same event type is required
        if event1.event_type != event2.event_type:
            return False
        
        # Calculate text similarity
        text1 = (event1.headline + " " + event1.summary).lower()
        text2 = (event2.headline + " " + event2.summary).lower()
        
        similarity = self._jaccard_similarity(text1, text2)
        
        return similarity >= self.similarity_threshold
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate Jaccard similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        # Extract words
        words1 = set(self._tokenize(text1))
        words2 = set(self._tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Simple word tokenization
        words = text.split()
        # Filter out very short words
        return [w for w in words if len(w) > 2]
