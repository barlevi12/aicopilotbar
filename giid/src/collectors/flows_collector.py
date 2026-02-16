"""Flows collector for ETF flows and COT data."""

from typing import List
import logging
from datetime import datetime, timedelta
import random

from .base_collector import BaseCollector
from ..normalize.schema import RawEvent


logger = logging.getLogger(__name__)


class FlowsCollector(BaseCollector):
    """Collector for capital flows data (ETF, COT)."""
    
    def __init__(self, config: dict = None):
        """Initialize flows collector."""
        super().__init__(config)
        self.data_sources = [
            "cftc.gov",
            "etf.com",
            "etfdb.com"
        ]
    
    async def collect(self) -> List[RawEvent]:
        """
        Collect capital flows data.
        
        Returns:
            List of raw flow events
        """
        events = []
        
        logger.info("FlowsCollector: Collecting capital flows data...")
        
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
        """Generate sample flow events."""
        now = datetime.utcnow()
        
        return [
            {
                'source': 'etfdb.com',
                'url': 'https://etfdb.com/flows',
                'timestamp': now - timedelta(hours=4),
                'headline': 'URA sees $250M inflow amid uranium supply concerns',
                'content': 'Global X Uranium ETF (URA) recorded $250M inflow over past week. Year-to-date inflows now exceed $1.2B.',
                'metadata': {
                    'ticker': 'URA',
                    'flow_type': 'inflow',
                    'amount': 250000000,
                    'period': 'weekly',
                    'sector': 'uranium'
                }
            },
            {
                'source': 'cftc.gov',
                'url': 'https://cftc.gov/cot',
                'timestamp': now - timedelta(hours=6),
                'headline': 'COT Report: Large speculators increase gold net long positions',
                'content': 'Non-commercial traders increased net long gold positions by 15% week-over-week, reaching highest level since 2020.',
                'metadata': {
                    'instrument': 'gold',
                    'trader_type': 'non-commercial',
                    'position_change': 15.0,
                    'direction': 'long'
                }
            }
        ]
