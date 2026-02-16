"""Impact scorer for events (0-120 scale)."""

from typing import Optional
import logging
import yaml
from pathlib import Path

from ..normalize.schema import NormalizedEvent, EventType


logger = logging.getLogger(__name__)


class ImpactScorer:
    """Scores events on a 0-120 scale based on multiple factors."""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize impact scorer.
        
        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir
        self.thresholds = self._load_thresholds()
        self.watchlists = self._load_watchlists()
    
    def _load_thresholds(self) -> dict:
        """Load scoring thresholds configuration."""
        if not self.config_dir:
            return {}
        
        config_path = Path(self.config_dir) / 'thresholds.yaml'
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Failed to load thresholds: {e}")
        return {}
    
    def _load_watchlists(self) -> dict:
        """Load watchlists configuration."""
        if not self.config_dir:
            return {}
        
        config_path = Path(self.config_dir) / 'watchlists.yaml'
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Failed to load watchlists: {e}")
        return {}
    
    def calculate(self, event: NormalizedEvent) -> int:
        """
        Calculate total impact score for an event.
        
        Args:
            event: Normalized event to score
            
        Returns:
            Impact score (0-120)
        """
        score = 0
        
        score += self.source_reliability(event)      # 0-20
        score += self.financial_magnitude(event)     # 0-25
        score += self.project_stage(event)           # 0-15
        score += self.regulatory_severity(event)     # 0-20
        score += self.thesis_relevance(event)        # 0-20
        score += self.institutional_signal(event)    # 0-20
        
        # Cap at 120
        return min(score, 120)
    
    def source_reliability(self, event: NormalizedEvent) -> int:
        """
        Score based on source reliability (0-20).
        
        Args:
            event: Event to score
            
        Returns:
            Source reliability score
        """
        tier_scores = {
            1: 20,  # Official/regulatory
            2: 15,  # Institutional
            3: 10,  # Reputable news
            4: 5    # Unverified
        }
        
        base_score = tier_scores.get(event.source_tier, 5)
        
        # Boost for high confidence
        if event.confidence.value == "high":
            return base_score
        elif event.confidence.value == "medium":
            return int(base_score * 0.9)
        else:
            return int(base_score * 0.7)
    
    def financial_magnitude(self, event: NormalizedEvent) -> int:
        """
        Score based on financial magnitude (0-25).
        
        Args:
            event: Event to score
            
        Returns:
            Financial magnitude score
        """
        # Extract amount from metadata
        amount = event.raw_data.get('metadata', {}).get('amount')
        
        if not amount:
            # Try to infer from content
            return 10  # Default medium score
        
        # Score based on thresholds
        if amount >= 10_000_000_000:  # $10B+
            return 25
        elif amount >= 5_000_000_000:  # $5B+
            return 20
        elif amount >= 1_000_000_000:  # $1B+
            return 15
        elif amount >= 500_000_000:    # $500M+
            return 10
        elif amount >= 100_000_000:    # $100M+
            return 5
        else:
            return 2
    
    def project_stage(self, event: NormalizedEvent) -> int:
        """
        Score based on project stage (0-15).
        
        Args:
            event: Event to score
            
        Returns:
            Project stage score
        """
        content_lower = (event.headline + " " + event.summary).lower()
        
        if any(word in content_lower for word in ['production', 'operating', 'commercial']):
            return 15
        elif any(word in content_lower for word in ['construction', 'building']):
            return 12
        elif any(word in content_lower for word in ['financing', 'funded', 'capital']):
            return 10
        elif any(word in content_lower for word in ['feasibility', 'study', 'assessment']):
            return 7
        elif any(word in content_lower for word in ['exploration', 'discovery']):
            return 5
        
        return 8  # Default mid-range
    
    def regulatory_severity(self, event: NormalizedEvent) -> int:
        """
        Score based on regulatory severity (0-20).
        
        Args:
            event: Event to score
            
        Returns:
            Regulatory severity score
        """
        if event.event_type not in [EventType.REGULATORY_APPROVAL, EventType.SANCTIONS, EventType.LICENSE_GRANT]:
            return 5  # Not regulatory
        
        content_lower = (event.headline + " " + event.summary).lower()
        
        if any(word in content_lower for word in ['revoked', 'revocation', 'suspended']):
            return 20
        elif any(word in content_lower for word in ['denied', 'rejection', 'sanction']):
            return 18
        elif any(word in content_lower for word in ['conditional', 'restricted']):
            return 12
        elif any(word in content_lower for word in ['approved', 'granted', 'license']):
            return 15
        elif any(word in content_lower for word in ['application', 'pending']):
            return 5
        
        return 10
    
    def thesis_relevance(self, event: NormalizedEvent) -> int:
        """
        Score based on investment thesis relevance (0-20).
        
        Args:
            event: Event to score
            
        Returns:
            Thesis relevance score
        """
        # Check if sector is in watchlist
        if not self.watchlists or 'sectors' not in self.watchlists:
            return 10
        
        priority_sectors = ['Uranium', 'Critical Minerals', 'Energy', 'Satellites']
        
        if event.sector in priority_sectors:
            return 20
        
        # Check keywords
        content_lower = (event.headline + " " + event.summary).lower()
        priority_keywords = ['uranium', 'lithium', 'rare earth', 'nuclear', 'critical minerals']
        
        if any(keyword in content_lower for keyword in priority_keywords):
            return 18
        
        # Related sector
        if event.sector in ['Financials']:
            return 12
        
        return 8
    
    def institutional_signal(self, event: NormalizedEvent) -> int:
        """
        Score based on institutional signal strength (0-20).
        
        Args:
            event: Event to score
            
        Returns:
            Institutional signal score
        """
        # Rating action
        if event.event_type == EventType.RATING_CHANGE:
            if event.institutional_source:
                return 20
            return 18
        
        # Tier-1 bank sector call
        if event.institutional_source and event.source_tier <= 2:
            content_lower = (event.headline + " " + event.summary).lower()
            if any(word in content_lower for word in ['outlook', 'upgrade', 'sector', 'overweight']):
                return 16
        
        # Thematic macro note
        if event.event_type in [EventType.GEOPOLITICAL_EVENT, EventType.FX_EVENT]:
            if event.source_tier <= 2:
                return 12
        
        # Research note
        if event.institutional_source:
            return 8
        
        return 0
