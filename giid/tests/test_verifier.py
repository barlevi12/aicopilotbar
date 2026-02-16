"""Tests for verification engine."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pytest
from datetime import datetime

from verify import VerificationEngine, SourceRanker
from normalize.schema import RawEvent, ConfidenceLevel


class TestVerifier:
    """Test suite for verification engine."""
    
    def test_source_ranker(self):
        """Test source ranking."""
        ranker = SourceRanker()
        
        # Tier 1 sources
        assert ranker.rank('sec.gov') == 1
        assert ranker.rank('moodys.com') == 1
        assert ranker.is_tier_1('sec.gov')
        
        # Tier 2 sources
        assert ranker.rank('goldmansachs.com') == 2
        assert ranker.is_institutional('jpmorgan.com')
        
        # Unknown source
        assert ranker.rank('unknown.com') == 4
    
    def test_verification_engine(self):
        """Test verification engine."""
        engine = VerificationEngine()
        
        raw_event = RawEvent(
            id='test_001',
            timestamp=datetime.utcnow(),
            source='sec.gov',
            url='https://sec.gov/test',
            headline='Test event',
            content='Test content'
        )
        
        verified = engine.verify(raw_event)
        
        assert verified.confidence == ConfidenceLevel.HIGH
        assert verified.source_tier == 1
        assert not verified.cross_checked
    
    def test_confidence_calculation(self):
        """Test confidence level calculation."""
        engine = VerificationEngine()
        
        # Tier 1 source = HIGH confidence
        assert engine._calculate_confidence(1, False, 0) == ConfidenceLevel.HIGH
        
        # Tier 2 with confirmation = HIGH
        assert engine._calculate_confidence(2, True, 2) == ConfidenceLevel.HIGH
        
        # Tier 2 without confirmation = MEDIUM
        assert engine._calculate_confidence(2, False, 0) == ConfidenceLevel.MEDIUM
        
        # Tier 3 = LOW
        assert engine._calculate_confidence(3, True, 1) == ConfidenceLevel.LOW
