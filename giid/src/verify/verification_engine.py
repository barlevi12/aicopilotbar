"""Verification engine for event validation."""

from typing import List
import logging

from ..normalize.schema import RawEvent, VerifiedEvent, ConfidenceLevel
from .source_ranker import SourceRanker
from .cross_checker import CrossChecker


logger = logging.getLogger(__name__)


class VerificationEngine:
    """Verifies events and assigns confidence levels."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize verification engine.
        
        Args:
            config_path: Path to configuration directory
        """
        self.source_ranker = SourceRanker(config_path)
        self.cross_checker = CrossChecker()
    
    def verify(self, event: RawEvent, all_events: List[RawEvent] = None) -> VerifiedEvent:
        """
        Verify a single event.
        
        Args:
            event: Raw event to verify
            all_events: List of all events for cross-checking
            
        Returns:
            Verified event with confidence level
        """
        # Check source tier
        source_tier = self.source_ranker.rank(event.source)
        
        # Cross-check with other sources
        all_events = all_events or []
        cross_checked, num_confirmations = self.cross_checker.check_event(event, all_events)
        
        # Determine confidence level
        confidence = self._calculate_confidence(source_tier, cross_checked, num_confirmations)
        
        # Build verification notes
        notes = self._build_verification_notes(source_tier, cross_checked, num_confirmations)
        
        return VerifiedEvent(
            raw_event=event,
            confidence=confidence,
            source_tier=source_tier,
            verification_notes=notes,
            cross_checked=cross_checked,
            num_confirmations=num_confirmations
        )
    
    def verify_batch(self, events: List[RawEvent]) -> List[VerifiedEvent]:
        """
        Verify a batch of events.
        
        Args:
            events: List of raw events
            
        Returns:
            List of verified events
        """
        verified_events = []
        
        for event in events:
            try:
                verified = self.verify(event, all_events=events)
                verified_events.append(verified)
            except Exception as e:
                logger.error(f"Failed to verify event {event.id}: {e}")
        
        logger.info(f"Verified {len(verified_events)} out of {len(events)} events")
        return verified_events
    
    def _calculate_confidence(
        self,
        source_tier: int,
        cross_checked: bool,
        num_confirmations: int
    ) -> ConfidenceLevel:
        """
        Calculate confidence level based on verification factors.
        
        Args:
            source_tier: Source tier (1-4)
            cross_checked: Whether event was cross-checked
            num_confirmations: Number of confirmations
            
        Returns:
            Confidence level
        """
        # Tier 1 source with confirmation = HIGH
        if source_tier == 1 and (cross_checked or num_confirmations >= 2):
            return ConfidenceLevel.HIGH
        
        # Tier 1 source without confirmation = HIGH
        if source_tier == 1:
            return ConfidenceLevel.HIGH
        
        # Tier 2 source with multiple confirmations = HIGH
        if source_tier == 2 and num_confirmations >= 2:
            return ConfidenceLevel.HIGH
        
        # Tier 2 source with confirmation = MEDIUM
        if source_tier == 2 and cross_checked:
            return ConfidenceLevel.MEDIUM
        
        # Tier 2 source without confirmation = MEDIUM
        if source_tier == 2:
            return ConfidenceLevel.MEDIUM
        
        # Tier 3 with confirmations = MEDIUM
        if source_tier == 3 and num_confirmations >= 2:
            return ConfidenceLevel.MEDIUM
        
        # Tier 3 with confirmation = LOW
        if source_tier == 3 and cross_checked:
            return ConfidenceLevel.LOW
        
        # Everything else = LOW
        return ConfidenceLevel.LOW
    
    def _build_verification_notes(
        self,
        source_tier: int,
        cross_checked: bool,
        num_confirmations: int
    ) -> str:
        """Build human-readable verification notes."""
        notes = [f"Source Tier: {source_tier}"]
        
        if cross_checked:
            notes.append(f"Cross-checked with {num_confirmations} source(s)")
        else:
            notes.append("No cross-verification available")
        
        if source_tier == 1:
            notes.append("Official/regulatory source")
        elif source_tier == 2:
            notes.append("Institutional source")
        
        return "; ".join(notes)
