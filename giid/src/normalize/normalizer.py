"""Event normalizer."""

from typing import List, Optional
import logging
import yaml
from pathlib import Path

from ..normalize.schema import (
    RawEvent, VerifiedEvent, NormalizedEvent,
    EventType, ConfidenceLevel, FlowSignal
)


logger = logging.getLogger(__name__)


class Normalizer:
    """Normalizes verified events to standard schema."""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize normalizer with configuration.
        
        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir
        self.watchlists = self._load_config('watchlists.yaml')
        self.people_config = self._load_config('people.yaml')
    
    def _load_config(self, filename: str) -> dict:
        """Load configuration file."""
        if not self.config_dir:
            return {}
        
        config_path = Path(self.config_dir) / filename
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Failed to load {filename}: {e}")
        return {}
    
    def normalize(self, verified_event: VerifiedEvent) -> NormalizedEvent:
        """
        Normalize a verified event.
        
        Args:
            verified_event: Verified event to normalize
            
        Returns:
            Normalized event
        """
        raw = verified_event.raw_event
        
        # Determine event type
        event_type = self._classify_event_type(raw)
        
        # Determine sector
        sector = self._identify_sector(raw)
        
        # Extract linked assets
        linked_assets = self._extract_assets(raw)
        
        # Extract mentioned people
        people_mentioned = self._extract_people(raw)
        
        # Identify region
        region = self._identify_region(raw)
        
        # Extract institutional source if any
        institutional_source = self._extract_institutional_source(raw)
        
        # Generate summary
        summary = self._generate_summary(raw)
        
        # Extract tags
        tags = self._extract_tags(raw)
        
        return NormalizedEvent(
            id=raw.id,
            timestamp=raw.timestamp,
            event_type=event_type,
            sector=sector,
            headline=raw.headline,
            summary=summary,
            source=raw.source,
            source_tier=verified_event.source_tier,
            confidence=verified_event.confidence,
            institutional_source=institutional_source,
            flow_signal=None,  # Added by flow engine
            impact_score=0,     # Added by scorer
            linked_assets=linked_assets,
            raw_data={
                'content': raw.content,
                'url': raw.url,
                'metadata': raw.metadata,
                'verification_notes': verified_event.verification_notes
            },
            tags=tags,
            region=region,
            people_mentioned=people_mentioned
        )
    
    def normalize_batch(self, verified_events: List[VerifiedEvent]) -> List[NormalizedEvent]:
        """Normalize a batch of verified events."""
        normalized_events = []
        
        for verified_event in verified_events:
            try:
                normalized = self.normalize(verified_event)
                normalized_events.append(normalized)
            except Exception as e:
                logger.error(f"Failed to normalize event {verified_event.raw_event.id}: {e}")
        
        logger.info(f"Normalized {len(normalized_events)} events")
        return normalized_events
    
    def _classify_event_type(self, event: RawEvent) -> EventType:
        """Classify event type based on content."""
        content_lower = (event.headline + " " + event.content).lower()
        
        # Check metadata first
        if 'event_type' in event.metadata:
            try:
                return EventType(event.metadata['event_type'])
            except:
                pass
        
        # Keyword-based classification
        if any(word in content_lower for word in ['upgrade', 'downgrade', 'rating', 'outlook']):
            return EventType.RATING_CHANGE
        elif any(word in content_lower for word in ['sanction', 'embargo']):
            return EventType.SANCTIONS
        elif any(word in content_lower for word in ['merger', 'acquisition', 'takeover']):
            return EventType.MERGER_ACQUISITION
        elif any(word in content_lower for word in ['license', 'approval', 'permit']):
            return EventType.REGULATORY_APPROVAL
        elif any(word in content_lower for word in ['ipo', 'public offering']):
            return EventType.IPO_ANNOUNCEMENT
        elif any(word in content_lower for word in ['inflow', 'outflow', 'cot', 'positioning']):
            return EventType.FLOW_SIGNAL
        elif any(word in content_lower for word in ['strait', 'canal', 'chokepoint', 'geopolitical']):
            return EventType.GEOPOLITICAL_EVENT
        
        return EventType.REGULATORY_APPROVAL
    
    def _identify_sector(self, event: RawEvent) -> str:
        """Identify which sector this event belongs to."""
        content_lower = (event.headline + " " + event.content).lower()
        
        # Check metadata first
        if 'sector' in event.metadata:
            return event.metadata['sector']
        
        # Check against watchlist sectors
        if self.watchlists and 'sectors' in self.watchlists:
            for sector_key, sector_config in self.watchlists['sectors'].items():
                keywords = sector_config.get('keywords', [])
                if any(keyword.lower() in content_lower for keyword in keywords):
                    return sector_config.get('name', sector_key)
        
        return "General"
    
    def _extract_assets(self, event: RawEvent) -> List[str]:
        """Extract linked assets/tickers."""
        assets = []
        
        # From metadata
        if 'ticker' in event.metadata:
            assets.append(event.metadata['ticker'])
        
        if 'tickers' in event.metadata:
            assets.extend(event.metadata['tickers'])
        
        return list(set(assets))
    
    def _extract_people(self, event: RawEvent) -> List[str]:
        """Extract mentioned people."""
        people = []
        content = event.headline + " " + event.content
        
        if self.people_config:
            for category in ['central_bankers', 'regulators', 'energy_executives', 'financial_executives']:
                if category in self.people_config:
                    for person in self.people_config[category]:
                        if person['name'] in content:
                            people.append(person['name'])
        
        return people
    
    def _identify_region(self, event: RawEvent) -> Optional[str]:
        """Identify geographic region."""
        if 'region' in event.metadata:
            return event.metadata['region']
        
        content_lower = (event.headline + " " + event.content).lower()
        
        regions = {
            'Middle East': ['middle east', 'persian gulf', 'iran', 'saudi', 'uae'],
            'Europe': ['europe', 'european', 'eu'],
            'Asia': ['asia', 'china', 'japan', 'india'],
            'United States': ['united states', 'u.s.', 'america']
        }
        
        for region, keywords in regions.items():
            if any(keyword in content_lower for keyword in keywords):
                return region
        
        return None
    
    def _extract_institutional_source(self, event: RawEvent) -> Optional[str]:
        """Extract institutional source name if present."""
        institutions = [
            'Goldman Sachs', 'JPMorgan', 'Morgan Stanley', 'UBS', 'Citigroup',
            'Bank of America', 'Deutsche Bank', "Moody's", 'S&P', 'Fitch'
        ]
        
        content = event.headline + " " + event.content
        for inst in institutions:
            if inst in content:
                return inst
        
        return None
    
    def _generate_summary(self, event: RawEvent) -> str:
        """Generate a concise summary."""
        # For now, use first 200 chars of content
        summary = event.content[:200]
        if len(event.content) > 200:
            summary += "..."
        return summary
    
    def _extract_tags(self, event: RawEvent) -> List[str]:
        """Extract relevant tags."""
        tags = []
        content_lower = (event.headline + " " + event.content).lower()
        
        tag_keywords = {
            'uranium': ['uranium', 'nuclear'],
            'lithium': ['lithium', 'battery'],
            'gold': ['gold'],
            'sanctions': ['sanction', 'embargo'],
            'rating': ['rating', 'upgrade', 'downgrade']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
