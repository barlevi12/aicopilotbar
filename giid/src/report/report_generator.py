"""Report generator for GIID system."""

from typing import List
import logging
from datetime import datetime

from ..normalize.schema import NormalizedEvent, FlowSignal, DailyReport


logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates various types of intelligence reports."""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize report generator.
        
        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir
    
    def generate_daily_report(
        self,
        events: List[NormalizedEvent],
        flow_signals: List[FlowSignal],
        report_date: datetime = None
    ) -> DailyReport:
        """
        Generate daily intelligence report.
        
        Args:
            events: List of normalized events
            flow_signals: List of flow signals
            report_date: Report date (defaults to now)
            
        Returns:
            Daily report structure
        """
        report_date = report_date or datetime.utcnow()
        
        # Filter high-impact events (score >= 70)
        material_events = [e for e in events if e.impact_score >= 70]
        material_events.sort(key=lambda e: e.impact_score, reverse=True)
        
        # Separate by type
        rating_actions = [e for e in material_events if 'rating' in e.event_type.value]
        institutional_calls = [e for e in material_events if e.institutional_source]
        geopolitical = [e for e in material_events if e.event_type.value == 'geopolitical_event']
        
        # Deep dive queue (score >= 80)
        deep_dive = [e for e in events if e.impact_score >= 80]
        deep_dive.sort(key=lambda e: e.impact_score, reverse=True)
        deep_dive = deep_dive[:5]  # Top 5
        
        # Generate executive summary
        exec_summary = self._generate_executive_summary(material_events, flow_signals)
        
        # Nothing material section
        nothing_material = self._identify_nothing_material(events)
        
        return DailyReport(
            report_date=report_date,
            executive_summary=exec_summary,
            material_events=material_events[:12],  # Top 12
            flow_signals=flow_signals,
            rating_actions=rating_actions,
            institutional_calls=institutional_calls,
            geopolitical_events=geopolitical,
            deep_dive_queue=deep_dive,
            nothing_material=nothing_material,
            metadata={
                'total_events': len(events),
                'material_events': len(material_events),
                'flow_signals': len(flow_signals)
            }
        )
    
    def _generate_executive_summary(
        self,
        material_events: List[NormalizedEvent],
        flow_signals: List[FlowSignal]
    ) -> str:
        """Generate executive summary (max 12 lines)."""
        lines = []
        
        # Summary header
        lines.append(f"## Executive Summary ({datetime.utcnow().strftime('%Y-%m-%d')})")
        lines.append("")
        
        # Key highlights
        if material_events:
            top_event = material_events[0]
            lines.append(f"**Top Event**: {top_event.headline} (Impact: {top_event.impact_score})")
        
        # Sector breakdown
        sectors = {}
        for event in material_events[:10]:
            sectors[event.sector] = sectors.get(event.sector, 0) + 1
        
        if sectors:
            top_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:3]
            sector_str = ", ".join([f"{s[0]} ({s[1]})" for s in top_sectors])
            lines.append(f"**Active Sectors**: {sector_str}")
        
        # Flow summary
        if flow_signals:
            high_mag_flows = [f for f in flow_signals if f.magnitude.value == 'high']
            if high_mag_flows:
                lines.append(f"**High-Magnitude Flows**: {len(high_mag_flows)} detected")
        
        # Material events count
        lines.append(f"**Material Events**: {len(material_events)} events scored ≥70")
        
        # Pad to ensure we don't exceed 12 lines
        while len(lines) < 12:
            lines.append("")
        
        return "\n".join(lines[:12])
    
    def _identify_nothing_material(self, events: List[NormalizedEvent]) -> List[str]:
        """Identify areas with no material developments."""
        nothing_material = []
        
        # Define key sectors to check
        key_sectors = ['Uranium', 'Critical Minerals', 'Energy', 'Satellites', 'Financials']
        
        # Check which sectors have no high-impact events
        for sector in key_sectors:
            sector_events = [e for e in events if e.sector == sector and e.impact_score >= 70]
            if not sector_events:
                nothing_material.append(f"No material developments in {sector}")
        
        return nothing_material
    
    def generate_alert(self, event: NormalizedEvent) -> str:
        """
        Generate alert for high-impact event.
        
        Args:
            event: Event to alert on
            
        Returns:
            Alert text
        """
        alert = f"""
# ALERT: {event.headline}

**Impact Score**: {event.impact_score}/120
**Sector**: {event.sector}
**Source**: {event.source} (Tier {event.source_tier})
**Confidence**: {event.confidence.value.upper()}

## Summary
{event.summary}

## Linked Assets
{', '.join(event.linked_assets) if event.linked_assets else 'None'}

## Tags
{', '.join(event.tags) if event.tags else 'None'}
"""
        return alert.strip()
