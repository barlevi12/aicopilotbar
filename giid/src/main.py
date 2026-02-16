"""Main entry point for GIID system."""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.collectors import (
    NewsCollector,
    RegulatoryCollector,
    RatingsCollector,
    FlowsCollector,
    FXMetalsCollector
)
from src.verify import VerificationEngine
from src.normalize import Normalizer
from src.dedup import Deduplicator, Clusterer
from src.score import ImpactScorer
from src.flows import FlowEngine
from src.report import DailyBriefGenerator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('giid.log')
    ]
)

logger = logging.getLogger(__name__)


async def run_giid():
    """Main GIID system execution."""
    logger.info("=" * 80)
    logger.info("GIID System Starting")
    logger.info("=" * 80)
    
    # Setup paths
    base_dir = Path(__file__).parent.parent  # Go up to giid/ directory
    config_dir = base_dir / 'config'
    data_dir = base_dir / 'data'
    reports_dir = base_dir / 'reports'
    
    # Create directories if they don't exist
    data_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    try:
        # Step 1: Collect from all sources
        logger.info("Step 1: Collecting data from all sources...")
        collectors = [
            NewsCollector(),
            RegulatoryCollector(),
            RatingsCollector(),
            FlowsCollector(),
            FXMetalsCollector()
        ]
        
        all_raw_events = []
        for collector in collectors:
            events = await collector.collect_with_retry()
            all_raw_events.extend(events)
        
        logger.info(f"Collected {len(all_raw_events)} raw events")
        
        # Step 2: Verify all events
        logger.info("Step 2: Verifying events...")
        verifier = VerificationEngine(str(config_dir))
        verified_events = verifier.verify_batch(all_raw_events)
        logger.info(f"Verified {len(verified_events)} events")
        
        # Step 3: Normalize to schema
        logger.info("Step 3: Normalizing events...")
        normalizer = Normalizer(str(config_dir))
        normalized_events = normalizer.normalize_batch(verified_events)
        logger.info(f"Normalized {len(normalized_events)} events")
        
        # Step 4: Deduplicate and cluster
        logger.info("Step 4: Deduplicating events...")
        deduplicator = Deduplicator()
        unique_events = deduplicator.dedupe(normalized_events)
        logger.info(f"Deduplicated to {len(unique_events)} unique events")
        
        logger.info("Step 5: Clustering related events...")
        clusterer = Clusterer()
        clusters = clusterer.cluster_related(unique_events)
        logger.info(f"Created {len(clusters)} event clusters")
        
        # Step 5: Score each event
        logger.info("Step 6: Scoring events...")
        scorer = ImpactScorer(str(config_dir))
        for event in unique_events:
            event.impact_score = scorer.calculate(event)
        
        # Sort by score
        unique_events.sort(key=lambda e: e.impact_score, reverse=True)
        logger.info(f"Scored all events. Top score: {unique_events[0].impact_score if unique_events else 0}")
        
        # Step 6: Analyze flows
        logger.info("Step 7: Analyzing capital flows...")
        flow_engine = FlowEngine(str(config_dir))
        flow_signals = flow_engine.analyze_events(unique_events)
        logger.info(f"Generated {len(flow_signals)} flow signals")
        
        # Step 7: Generate report
        logger.info("Step 8: Generating daily brief...")
        brief_generator = DailyBriefGenerator(str(config_dir))
        
        report_timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        report_path = reports_dir / f"daily_brief_{report_timestamp}.md"
        
        markdown_report = brief_generator.generate(
            unique_events,
            flow_signals,
            str(report_path)
        )
        
        logger.info(f"Report saved to: {report_path}")
        
        # Step 8: Save data
        logger.info("Step 9: Saving processed data...")
        
        # Save events to JSON
        events_data = []
        for event in unique_events:
            events_data.append({
                'id': event.id,
                'timestamp': event.timestamp.isoformat(),
                'event_type': event.event_type.value,
                'sector': event.sector,
                'headline': event.headline,
                'summary': event.summary,
                'source': event.source,
                'source_tier': event.source_tier,
                'confidence': event.confidence.value,
                'impact_score': event.impact_score,
                'linked_assets': event.linked_assets,
                'tags': event.tags
            })
        
        data_path = data_dir / f"events_{report_timestamp}.json"
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(events_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Events data saved to: {data_path}")
        
        # Print summary
        logger.info("=" * 80)
        logger.info("GIID System Execution Complete")
        logger.info(f"Total events processed: {len(all_raw_events)}")
        logger.info(f"Unique events: {len(unique_events)}")
        logger.info(f"Material events (score ≥70): {len([e for e in unique_events if e.impact_score >= 70])}")
        logger.info(f"Flow signals: {len(flow_signals)}")
        logger.info(f"Report: {report_path}")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"Error during GIID execution: {e}", exc_info=True)
        return False


def main():
    """Main entry point."""
    success = asyncio.run(run_giid())
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
