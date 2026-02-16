"""Daily brief generator."""

import logging
from datetime import datetime
from pathlib import Path
from typing import List

from ..normalize.schema import NormalizedEvent, FlowSignal, DailyReport
from .report_generator import ReportGenerator


logger = logging.getLogger(__name__)


class DailyBriefGenerator:
    """Generates daily intelligence briefs in Markdown format."""
    
    def __init__(self, config_dir: str = None, template_dir: str = None):
        """
        Initialize daily brief generator.
        
        Args:
            config_dir: Path to configuration directory
            template_dir: Path to templates directory
        """
        self.config_dir = config_dir
        self.template_dir = template_dir
        self.report_generator = ReportGenerator(config_dir)
    
    def generate(
        self,
        events: List[NormalizedEvent],
        flows: List[FlowSignal],
        output_path: str = None
    ) -> str:
        """
        Generate daily brief report.
        
        Args:
            events: List of normalized events
            flows: List of flow signals
            output_path: Optional path to save report
            
        Returns:
            Markdown report content
        """
        # Generate report structure
        report = self.report_generator.generate_daily_report(events, flows)
        
        # Build markdown content
        markdown = self._build_markdown(report)
        
        # Save if output path provided
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            logger.info(f"Saved daily brief to {output_path}")
        
        return markdown
    
    def _build_markdown(self, report: DailyReport) -> str:
        """Build markdown report from report structure."""
        lines = []
        
        # Header
        lines.append("# GIID Daily Intelligence Brief")
        lines.append(f"**Date**: {report.report_date.strftime('%Y-%m-%d %H:%M UTC')}")
        lines.append(f"**Timezone**: Asia/Jerusalem")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Executive Summary
        lines.append(report.executive_summary)
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Material Events
        if report.material_events:
            lines.append("## Material Events (Top-10)")
            lines.append("")
            lines.append(self._generate_events_table(report.material_events[:10]))
            lines.append("")
        
        # Institutional & Rating Signals
        if report.rating_actions or report.institutional_calls:
            lines.append("## Institutional & Rating Signals")
            lines.append("")
            
            if report.rating_actions:
                lines.append("### Rating Actions")
                lines.append("")
                for event in report.rating_actions[:5]:
                    lines.append(f"- **{event.headline}** (Score: {event.impact_score})")
                    lines.append(f"  - Source: {event.institutional_source or event.source}")
                    lines.append(f"  - Confidence: {event.confidence.value}")
                    lines.append("")
            
            if report.institutional_calls:
                lines.append("### Institutional Calls")
                lines.append("")
                for event in report.institutional_calls[:5]:
                    lines.append(f"- **{event.headline}** (Score: {event.impact_score})")
                    lines.append(f"  - Institution: {event.institutional_source}")
                    lines.append(f"  - Sector: {event.sector}")
                    lines.append("")
        
        # Capital Flows & IPOs
        if report.flow_signals:
            lines.append("## Capital Flows & IPOs")
            lines.append("")
            lines.append(self._generate_flows_table(report.flow_signals))
            lines.append("")
        
        # Geopolitics & Regulation
        if report.geopolitical_events:
            lines.append("## Geopolitics & Regulation")
            lines.append("")
            for event in report.geopolitical_events[:5]:
                lines.append(f"- **{event.headline}** (Score: {event.impact_score})")
                if event.region:
                    lines.append(f"  - Region: {event.region}")
                lines.append(f"  - {event.summary}")
                lines.append("")
        
        # Deep-Dive Queue
        if report.deep_dive_queue:
            lines.append("## Deep-Dive Queue (Score ≥80)")
            lines.append("")
            for i, event in enumerate(report.deep_dive_queue, 1):
                lines.append(f"{i}. **{event.headline}** (Score: {event.impact_score})")
                lines.append(f"   - Sector: {event.sector}")
                lines.append(f"   - Source: {event.source}")
                lines.append("")
        
        # Nothing Material
        if report.nothing_material:
            lines.append("## Nothing Material")
            lines.append("")
            for item in report.nothing_material:
                lines.append(f"- {item}")
            lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append(f"*Report generated by GIID System*")
        lines.append(f"*Total events analyzed: {report.metadata.get('total_events', 0)}*")
        
        return "\n".join(lines)
    
    def _generate_events_table(self, events: List[NormalizedEvent]) -> str:
        """Generate markdown table for events."""
        lines = []
        lines.append("| Score | Sector | Headline | Source |")
        lines.append("|-------|--------|----------|--------|")
        
        for event in events:
            headline = event.headline[:60] + "..." if len(event.headline) > 60 else event.headline
            source = event.institutional_source or event.source.split('.')[0]
            lines.append(f"| {event.impact_score} | {event.sector} | {headline} | {source} |")
        
        return "\n".join(lines)
    
    def _generate_flows_table(self, flows: List[FlowSignal]) -> str:
        """Generate markdown table for flows."""
        lines = []
        lines.append("| Type | Magnitude | Assets | Description |")
        lines.append("|------|-----------|--------|-------------|")
        
        for flow in flows[:10]:
            flow_type = flow.type.value.replace('_', ' ').title()
            assets = ', '.join(flow.linked_assets[:3])
            desc = flow.description[:50] + "..." if len(flow.description) > 50 else flow.description
            lines.append(f"| {flow_type} | {flow.magnitude.value} | {assets} | {desc} |")
        
        return "\n".join(lines)
