#!/usr/bin/env python
"""
Simple test runner to demonstrate GIID system functionality.
For full unit tests, install the package with: pip install -e .
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("✓ Testing imports...")
    
    try:
        from collectors import NewsCollector, RatingsCollector
        from verify import VerificationEngine
        from normalize import Normalizer
        from score import ImpactScorer
        from flows import FlowEngine
        from report import DailyBriefGenerator
        print("  ✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_collectors():
    """Test collector functionality."""
    print("✓ Testing collectors...")
    
    try:
        import asyncio
        from collectors import NewsCollector
        
        collector = NewsCollector()
        events = asyncio.run(collector.collect())
        
        print(f"  ✓ Collected {len(events)} events")
        return True
    except Exception as e:
        print(f"  ✗ Collector test failed: {e}")
        return False


def test_verification():
    """Test verification engine."""
    print("✓ Testing verification engine...")
    
    try:
        from verify import SourceRanker
        
        ranker = SourceRanker()
        
        assert ranker.rank('sec.gov') == 1
        assert ranker.rank('goldmansachs.com') == 2
        assert ranker.is_tier_1('moodys.com')
        
        print("  ✓ Source ranking works correctly")
        return True
    except Exception as e:
        print(f"  ✗ Verification test failed: {e}")
        return False


def test_scoring():
    """Test impact scoring."""
    print("✓ Testing impact scorer...")
    
    try:
        from datetime import datetime
        from score import ImpactScorer
        from normalize.schema import NormalizedEvent, EventType, ConfidenceLevel
        
        scorer = ImpactScorer()
        
        event = NormalizedEvent(
            id='test',
            timestamp=datetime.utcnow(),
            event_type=EventType.RATING_CHANGE,
            sector='Uranium',
            headline='Test',
            summary='Test',
            source='moodys.com',
            source_tier=1,
            confidence=ConfidenceLevel.HIGH,
            institutional_source="Moody's"
        )
        
        score = scorer.calculate(event)
        assert 0 <= score <= 120
        
        print(f"  ✓ Scoring works (sample score: {score})")
        return True
    except Exception as e:
        print(f"  ✗ Scoring test failed: {e}")
        return False


def test_report_generation():
    """Test report generation."""
    print("✓ Testing report generation...")
    
    try:
        from datetime import datetime
        from report import ReportGenerator
        from normalize.schema import NormalizedEvent, EventType, ConfidenceLevel
        
        generator = ReportGenerator()
        
        events = [
            NormalizedEvent(
                id='test',
                timestamp=datetime.utcnow(),
                event_type=EventType.RATING_CHANGE,
                sector='Uranium',
                headline='Test Event',
                summary='Test',
                source='moodys.com',
                source_tier=1,
                confidence=ConfidenceLevel.HIGH,
                institutional_source="Moody's",
                impact_score=85
            )
        ]
        
        report = generator.generate_daily_report(events, [])
        
        assert report is not None
        assert len(report.material_events) == 1
        
        print("  ✓ Report generation works")
        return True
    except Exception as e:
        print(f"  ✗ Report generation test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("GIID System - Quick Tests")
    print("="*60)
    print()
    
    tests = [
        test_imports,
        test_collectors,
        test_verification,
        test_scoring,
        test_report_generation,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("="*60)
    passed = sum(results)
    total = len(results)
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
