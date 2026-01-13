"""FX and metals collector for currency and precious metals data."""

from typing import List
import logging
from datetime import datetime, timedelta

from .base_collector import BaseCollector
from ..normalize.schema import RawEvent


logger = logging.getLogger(__name__)


class FXMetalsCollector(BaseCollector):
    """Collector for FX and precious metals events."""
    
    def __init__(self, config: dict = None):
        """Initialize FX and metals collector."""
        super().__init__(config)
        self.data_sources = [
            "federalreserve.gov",
            "ecb.europa.eu",
            "kitco.com",
            "lbma.org.uk"
        ]
    
    async def collect(self) -> List[RawEvent]:
        """
        Collect FX and precious metals events.
        
        Returns:
            List of raw FX/metals events
        """
        events = []
        
        logger.info("FXMetalsCollector: Collecting FX and metals data...")
        
        sample_events = self._generate_sample_events()
        
        for event_data in sample_events:
            event = RawEvent(
                id=self.create_event_id(
                    event_data['source'],
                    event_data['timestamp'],
                    event_data['headline']
                ),
                timestamp=event_data['timestamp'],
                source=event_data['source'],
                url=event_data.get('url'),
                headline=event_data['headline'],
                content=event_data['content'],
                metadata=event_data.get('metadata', {})
            )
            events.append(event)
        
        return events
    
    def _generate_sample_events(self) -> List[dict]:
        """Generate sample FX and metals events."""
        now = datetime.utcnow()
        
        return [
            {
                'source': 'lbma.org.uk',
                'url': 'https://lbma.org.uk/prices',
                'timestamp': now - timedelta(hours=2),
                'headline': 'Gold breaks above $2,100/oz on geopolitical tensions',
                'content': 'Gold prices surged 2.5% to reach $2,120/oz amid escalating Middle East tensions and safe-haven demand.',
                'metadata': {
                    'metal': 'gold',
                    'price': 2120.0,
                    'change_percent': 2.5,
                    'catalyst': 'geopolitical'
                }
            }
        ]
