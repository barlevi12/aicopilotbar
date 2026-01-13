"""Tests for report generator."""

import pytest
from datetime import datetime

from report import ReportGenerator, DailyBriefGenerator
from normalize.schema import NormalizedEvent, EventType, ConfidenceLevel, FlowSignal, FlowType, FlowMagnitude


class TestReporter:
    """Test suite for report generator."""
    
    def create_sample_event(self, score=75):
        """Create sample event."""
        return NormalizedEvent(
            id='test_001',
            timestamp=datetime.utcnow(),
            event_type=EventType.RATING_CHANGE,
            sector='Uranium',
            headline='Test headline',
            summary='Test summary',
            source='moodys.com',
            source_tier=1,
            confidence=ConfidenceLevel.HIGH,
            institutional_source="Moody's",
            impact_score=score,
            linked_assets=['URA'],
            raw_data={}
        )
    
    def create_sample_flow(self):
        """Create sample flow signal."""
        return FlowSignal(
            type=FlowType.EQUITY_INFLOW,
            magnitude=FlowMagnitude.HIGH,
            linked_assets=['URA'],
            amount=250_000_000,
            description='Test flow'
        )
    
    def test_report_generator_initialization(self):
        """Test report generator initialization."""
        generator = ReportGenerator()
        assert generator is not None
    
    def test_daily_report_generation(self):
        """Test daily report generation."""
        generator = ReportGenerator()
        
        events = [
            self.create_sample_event(score=90),
            self.create_sample_event(score=75),
            self.create_sample_event(score=60),
        ]
        
        flows = [self.create_sample_flow()]
        
        report = generator.generate_daily_report(events, flows)
        
        assert report is not None
        assert report.report_date is not None
        assert isinstance(report.material_events, list)
        assert isinstance(report.flow_signals, list)
        assert len(report.material_events) == 2  # Only score >= 70
    
    def test_executive_summary(self):
        """Test executive summary generation."""
        generator = ReportGenerator()
        
        events = [self.create_sample_event(score=90)]
        flows = [self.create_sample_flow()]
        
        summary = generator._generate_executive_summary(events, flows)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_daily_brief_markdown(self):
        """Test daily brief markdown generation."""
        generator = DailyBriefGenerator()
        
        events = [self.create_sample_event(score=90)]
        flows = [self.create_sample_flow()]
        
        markdown = generator.generate(events, flows)
        
        assert isinstance(markdown, str)
        assert '# GIID Daily Intelligence Brief' in markdown
        assert 'Material Events' in markdown
