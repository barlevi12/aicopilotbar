"""Tests for impact scorer."""

import pytest
from datetime import datetime

from score import ImpactScorer
from normalize.schema import NormalizedEvent, EventType, ConfidenceLevel


class TestScorer:
    """Test suite for impact scorer."""
    
    def create_sample_event(self, **kwargs):
        """Create a sample event for testing."""
        defaults = {
            'id': 'test_001',
            'timestamp': datetime.utcnow(),
            'event_type': EventType.RATING_CHANGE,
            'sector': 'Uranium',
            'headline': 'Test headline',
            'summary': 'Test summary',
            'source': 'moodys.com',
            'source_tier': 1,
            'confidence': ConfidenceLevel.HIGH,
            'institutional_source': "Moody's",
            'impact_score': 0,
            'linked_assets': [],
            'raw_data': {}
        }
        defaults.update(kwargs)
        return NormalizedEvent(**defaults)
    
    def test_source_reliability_scoring(self):
        """Test source reliability scoring."""
        scorer = ImpactScorer()
        
        # Tier 1 source
        event = self.create_sample_event(source_tier=1)
        score = scorer.source_reliability(event)
        assert score == 20
        
        # Tier 2 source
        event = self.create_sample_event(source_tier=2)
        score = scorer.source_reliability(event)
        assert score == 15
    
    def test_financial_magnitude_scoring(self):
        """Test financial magnitude scoring."""
        scorer = ImpactScorer()
        
        # Large deal ($10B+)
        event = self.create_sample_event(
            raw_data={'metadata': {'amount': 10_000_000_000}}
        )
        score = scorer.financial_magnitude(event)
        assert score == 25
        
        # Medium deal ($1B)
        event = self.create_sample_event(
            raw_data={'metadata': {'amount': 1_000_000_000}}
        )
        score = scorer.financial_magnitude(event)
        assert score == 15
    
    def test_institutional_signal_scoring(self):
        """Test institutional signal scoring."""
        scorer = ImpactScorer()
        
        # Rating action
        event = self.create_sample_event(
            event_type=EventType.RATING_CHANGE,
            institutional_source="Moody's"
        )
        score = scorer.institutional_signal(event)
        assert score == 20
    
    def test_total_score_calculation(self):
        """Test total impact score calculation."""
        scorer = ImpactScorer()
        
        event = self.create_sample_event(
            source_tier=1,
            event_type=EventType.RATING_CHANGE,
            institutional_source="Moody's",
            sector='Uranium',
            raw_data={'metadata': {'amount': 1_000_000_000}}
        )
        
        total_score = scorer.calculate(event)
        
        # Should be high score for Tier-1 rating action in priority sector
        assert total_score >= 80
        assert total_score <= 120
