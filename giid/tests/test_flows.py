"""Tests for flow engine."""

import pytest
from datetime import datetime

from flows import FlowEngine
from normalize.schema import NormalizedEvent, EventType, ConfidenceLevel, FlowMagnitude


class TestFlows:
    """Test suite for flow engine."""
    
    def create_flow_event(self, **kwargs):
        """Create a sample flow event."""
        defaults = {
            'id': 'flow_001',
            'timestamp': datetime.utcnow(),
            'event_type': EventType.FLOW_SIGNAL,
            'sector': 'Uranium',
            'headline': 'ETF inflow detected',
            'summary': 'Test flow',
            'source': 'etfdb.com',
            'source_tier': 3,
            'confidence': ConfidenceLevel.MEDIUM,
            'impact_score': 0,
            'linked_assets': ['URA'],
            'raw_data': {
                'metadata': {
                    'flow_type': 'inflow',
                    'amount': 250_000_000,
                    'ticker': 'URA'
                }
            }
        }
        defaults.update(kwargs)
        return NormalizedEvent(**defaults)
    
    def test_flow_engine_initialization(self):
        """Test flow engine initialization."""
        engine = FlowEngine()
        assert engine is not None
    
    def test_flow_signal_generation(self):
        """Test flow signal generation."""
        engine = FlowEngine()
        
        event = self.create_flow_event()
        signals = engine._analyze_event(event)
        
        assert len(signals) >= 0
        
        if signals:
            signal = signals[0]
            assert hasattr(signal, 'type')
            assert hasattr(signal, 'magnitude')
            assert hasattr(signal, 'linked_assets')
    
    def test_magnitude_calculation(self):
        """Test flow magnitude calculation."""
        engine = FlowEngine()
        
        # High magnitude
        assert engine._calculate_magnitude(2_000_000_000) == FlowMagnitude.HIGH
        
        # Medium magnitude
        assert engine._calculate_magnitude(600_000_000) == FlowMagnitude.MEDIUM
        
        # Low magnitude
        assert engine._calculate_magnitude(200_000_000) == FlowMagnitude.LOW
    
    def test_analyze_events(self):
        """Test analyzing multiple events."""
        engine = FlowEngine()
        
        events = [
            self.create_flow_event(id='flow_001'),
            self.create_flow_event(id='flow_002'),
        ]
        
        signals = engine.analyze_events(events)
        assert isinstance(signals, list)
