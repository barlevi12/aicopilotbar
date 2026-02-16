"""Base collector abstract class for all data collectors."""

from abc import ABC, abstractmethod
from typing import List, Optional
import asyncio
import logging
from datetime import datetime

from ..normalize.schema import RawEvent


logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """Base class for all data collectors with async support."""
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the base collector.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self.last_collection = None
        
    @abstractmethod
    async def collect(self) -> List[RawEvent]:
        """
        Collect raw events from the data source.
        
        Returns:
            List of raw events collected
        """
        pass
    
    def validate_source(self, source: str) -> bool:
        """
        Validate if the source is trusted.
        
        Args:
            source: Source URL or identifier
            
        Returns:
            True if source is valid/trusted
        """
        if not source:
            return False
            
        # Basic validation - can be overridden by subclasses
        trusted_domains = self.config.get('trusted_domains', [])
        if trusted_domains:
            return any(domain in source for domain in trusted_domains)
        
        return True
    
    async def collect_with_retry(self, max_retries: int = 3, delay: float = 1.0) -> List[RawEvent]:
        """
        Collect events with retry logic.
        
        Args:
            max_retries: Maximum number of retry attempts
            delay: Delay between retries in seconds
            
        Returns:
            List of collected raw events
        """
        for attempt in range(max_retries):
            try:
                events = await self.collect()
                self.last_collection = datetime.utcnow()
                logger.info(f"{self.name}: Collected {len(events)} events")
                return events
            except Exception as e:
                logger.warning(f"{self.name}: Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay * (attempt + 1))
                else:
                    logger.error(f"{self.name}: All retry attempts failed")
                    raise
        
        return []
    
    def filter_by_keywords(self, content: str, keywords: List[str]) -> bool:
        """
        Check if content contains any of the specified keywords.
        
        Args:
            content: Text content to check
            keywords: List of keywords to search for
            
        Returns:
            True if any keyword is found
        """
        content_lower = content.lower()
        return any(keyword.lower() in content_lower for keyword in keywords)
    
    def create_event_id(self, source: str, timestamp: datetime, headline: str) -> str:
        """
        Create a unique event ID.
        
        Args:
            source: Source of the event
            timestamp: Event timestamp
            headline: Event headline
            
        Returns:
            Unique event identifier
        """
        import hashlib
        
        # Create a hash from source, timestamp, and headline
        content = f"{source}:{timestamp.isoformat()}:{headline}"
        return hashlib.md5(content.encode()).hexdigest()
