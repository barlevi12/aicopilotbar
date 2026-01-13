"""Tests for collectors module."""

import pytest
import asyncio
from datetime import datetime

from collectors import NewsCollector, RegulatoryCollector, RatingsCollector


class TestCollectors:
    """Test suite for data collectors."""
    
    @pytest.mark.asyncio
    async def test_news_collector(self):
        """Test news collector."""
        collector = NewsCollector()
        events = await collector.collect()
        
        assert isinstance(events, list)
        assert len(events) >= 0
        
        if events:
            event = events[0]
            assert hasattr(event, 'id')
            assert hasattr(event, 'timestamp')
            assert hasattr(event, 'headline')
            assert hasattr(event, 'source')
    
    @pytest.mark.asyncio
    async def test_regulatory_collector(self):
        """Test regulatory collector."""
        collector = RegulatoryCollector()
        events = await collector.collect()
        
        assert isinstance(events, list)
    
    @pytest.mark.asyncio
    async def test_ratings_collector(self):
        """Test ratings collector."""
        collector = RatingsCollector()
        events = await collector.collect()
        
        assert isinstance(events, list)
    
    def test_source_validation(self):
        """Test source validation."""
        collector = NewsCollector()
        
        assert collector.validate_source('sec.gov')
        assert collector.validate_source('https://www.sec.gov/edgar')
    
    def test_event_id_generation(self):
        """Test event ID generation."""
        collector = NewsCollector()
        
        id1 = collector.create_event_id('source1', datetime.utcnow(), 'headline1')
        id2 = collector.create_event_id('source2', datetime.utcnow(), 'headline2')
        
        assert id1 != id2
        assert len(id1) == 32  # MD5 hash length
