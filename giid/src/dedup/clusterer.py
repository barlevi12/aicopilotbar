"""Event clusterer for related events."""

from typing import List
import logging
from datetime import datetime

from ..normalize.schema import NormalizedEvent, EventCluster


logger = logging.getLogger(__name__)


class Clusterer:
    """Clusters related events together."""
    
    def __init__(self, clustering_threshold: float = 0.70):
        """
        Initialize clusterer.
        
        Args:
            clustering_threshold: Threshold for clustering events (0-1)
        """
        self.clustering_threshold = clustering_threshold
    
    def cluster_related(self, events: List[NormalizedEvent]) -> List[EventCluster]:
        """
        Cluster related events.
        
        Args:
            events: List of events to cluster
            
        Returns:
            List of event clusters
        """
        if not events:
            return []
        
        clusters = []
        clustered_ids = set()
        
        for event in events:
            if event.id in clustered_ids:
                continue
            
            # Find related events
            related = self._find_related(event, events, clustered_ids)
            
            if related:
                # Create cluster
                cluster = self._create_cluster(event, related)
                clusters.append(cluster)
                
                # Mark as clustered
                clustered_ids.add(event.id)
                for rel_event in related:
                    clustered_ids.add(rel_event.id)
            else:
                # Single event cluster
                cluster = EventCluster(
                    cluster_id=f"cluster_{event.id}",
                    primary_event=event,
                    related_events=[],
                    cluster_summary=event.headline,
                    max_impact_score=event.impact_score,
                    timestamp=event.timestamp
                )
                clusters.append(cluster)
                clustered_ids.add(event.id)
        
        logger.info(f"Clustered {len(events)} events into {len(clusters)} clusters")
        return clusters
    
    def _find_related(
        self,
        primary_event: NormalizedEvent,
        all_events: List[NormalizedEvent],
        exclude_ids: set
    ) -> List[NormalizedEvent]:
        """Find events related to the primary event."""
        related = []
        
        for event in all_events:
            if event.id == primary_event.id or event.id in exclude_ids:
                continue
            
            if self._are_related(primary_event, event):
                related.append(event)
        
        return related
    
    def _are_related(self, event1: NormalizedEvent, event2: NormalizedEvent) -> bool:
        """Check if two events are related."""
        # Same sector
        if event1.sector != event2.sector:
            return False
        
        # Calculate similarity
        text1 = (event1.headline + " " + event1.summary).lower()
        text2 = (event2.headline + " " + event2.summary).lower()
        
        similarity = self._calculate_similarity(text1, text2)
        
        return similarity >= self.clustering_threshold
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _create_cluster(
        self,
        primary_event: NormalizedEvent,
        related_events: List[NormalizedEvent]
    ) -> EventCluster:
        """Create an event cluster."""
        # Find max impact score
        all_scores = [primary_event.impact_score] + [e.impact_score for e in related_events]
        max_score = max(all_scores)
        
        # Generate cluster summary
        summary = f"{primary_event.headline} (+{len(related_events)} related)"
        
        return EventCluster(
            cluster_id=f"cluster_{primary_event.id}",
            primary_event=primary_event,
            related_events=related_events,
            cluster_summary=summary,
            max_impact_score=max_score,
            timestamp=primary_event.timestamp
        )
