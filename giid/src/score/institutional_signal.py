"""Institutional signal detection and scoring."""

from typing import List, Optional
import logging

from ..normalize.schema import NormalizedEvent, EventType


logger = logging.getLogger(__name__)


class InstitutionalSignal:
    """Detects and scores institutional signals."""
    
    TIER_1_BANKS = [
        'Goldman Sachs', 'JPMorgan', 'Morgan Stanley', 'UBS',
        'Citigroup', 'Bank of America', 'Deutsche Bank'
    ]
    
    RATING_AGENCIES = ["Moody's", 'S&P', 'Fitch']
    
    def __init__(self):
        """Initialize institutional signal detector."""
        pass
    
    def detect_signal_type(self, event: NormalizedEvent) -> Optional[str]:
        """
        Detect type of institutional signal.
        
        Args:
            event: Event to analyze
            
        Returns:
            Signal type or None
        """
        # Rating agency action
        if any(agency in (event.institutional_source or '') for agency in self.RATING_AGENCIES):
            if event.event_type == EventType.RATING_CHANGE:
                return 'rating_action'
        
        # Tier-1 bank sector call
        if any(bank in (event.institutional_source or '') for bank in self.TIER_1_BANKS):
            content_lower = (event.headline + " " + event.summary).lower()
            if any(word in content_lower for word in ['sector', 'overweight', 'underweight', 'upgrade', 'downgrade']):
                return 'sector_call'
        
        # Macro thematic note
        if event.source_tier <= 2:
            content_lower = (event.headline + " " + event.summary).lower()
            if any(word in content_lower for word in ['macro', 'outlook', 'forecast', 'economy']):
                return 'macro_note'
        
        return None
    
    def score_institutional_signal(self, event: NormalizedEvent) -> int:
        """
        Score the strength of institutional signal.
        
        Args:
            event: Event to score
            
        Returns:
            Signal strength score (0-20)
        """
        signal_type = self.detect_signal_type(event)
        
        if not signal_type:
            return 0
        
        if signal_type == 'rating_action':
            return 18
        elif signal_type == 'sector_call':
            return 15
        elif signal_type == 'macro_note':
            return 12
        
        return 5
    
    def extract_institutional_calls(self, events: List[NormalizedEvent]) -> List[NormalizedEvent]:
        """
        Extract events that contain institutional calls.
        
        Args:
            events: List of events to filter
            
        Returns:
            List of events with institutional signals
        """
        institutional_events = []
        
        for event in events:
            if self.detect_signal_type(event):
                institutional_events.append(event)
        
        logger.info(f"Found {len(institutional_events)} institutional signals")
        return institutional_events
