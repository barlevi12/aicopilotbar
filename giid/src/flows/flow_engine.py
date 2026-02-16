"""Flow engine for analyzing capital flows."""

from typing import List
import logging
import yaml
from pathlib import Path

from ..normalize.schema import NormalizedEvent, FlowSignal, FlowType, FlowMagnitude, EventType


logger = logging.getLogger(__name__)


class FlowEngine:
    """Analyzes capital flows and generates flow signals."""
    
    def __init__(self, config_dir: str = None):
        """
        Initialize flow engine.
        
        Args:
            config_dir: Path to configuration directory
        """
        self.config_dir = config_dir
        self.flows_config = self._load_config('flows.yaml')
        self.thresholds = self._load_config('thresholds.yaml')
    
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
    
    def analyze_events(self, events: List[NormalizedEvent]) -> List[FlowSignal]:
        """
        Analyze events and generate flow signals.
        
        Args:
            events: List of normalized events
            
        Returns:
            List of flow signals
        """
        flow_signals = []
        
        # Extract flow events
        flow_events = [e for e in events if e.event_type == EventType.FLOW_SIGNAL]
        
        for event in flow_events:
            signals = self._analyze_event(event)
            flow_signals.extend(signals)
        
        logger.info(f"Generated {len(flow_signals)} flow signals from {len(flow_events)} events")
        return flow_signals
    
    def _analyze_event(self, event: NormalizedEvent) -> List[FlowSignal]:
        """Analyze a single event for flow signals."""
        signals = []
        
        metadata = event.raw_data.get('metadata', {})
        
        # Check for ETF flows
        if 'flow_type' in metadata:
            flow_type = metadata['flow_type']
            amount = metadata.get('amount', 0)
            
            # Determine flow type enum
            if flow_type == 'inflow':
                flow_type_enum = FlowType.EQUITY_INFLOW
            elif flow_type == 'outflow':
                flow_type_enum = FlowType.EQUITY_OUTFLOW
            else:
                flow_type_enum = FlowType.EQUITY_INFLOW
            
            # Determine magnitude
            magnitude = self._calculate_magnitude(amount)
            
            # Extract linked assets
            linked_assets = event.linked_assets or []
            if event.sector:
                linked_assets.append(event.sector.lower())
            
            signal = FlowSignal(
                type=flow_type_enum,
                magnitude=magnitude,
                linked_assets=linked_assets,
                amount=amount,
                description=f"{flow_type.title()} of ${amount:,.0f} in {event.sector}"
            )
            signals.append(signal)
        
        # Check for COT positioning
        elif 'position_change' in metadata:
            position_change = metadata['position_change']
            direction = metadata.get('direction', 'long')
            instrument = metadata.get('instrument', 'unknown')
            
            # Determine flow type
            if direction == 'long' and position_change > 0:
                flow_type_enum = FlowType.RISK_ON
            elif direction == 'short' and position_change > 0:
                flow_type_enum = FlowType.RISK_OFF
            else:
                flow_type_enum = FlowType.ROTATION
            
            # Determine magnitude based on position change percentage
            if abs(position_change) >= 20:
                magnitude = FlowMagnitude.HIGH
            elif abs(position_change) >= 10:
                magnitude = FlowMagnitude.MEDIUM
            else:
                magnitude = FlowMagnitude.LOW
            
            signal = FlowSignal(
                type=flow_type_enum,
                magnitude=magnitude,
                linked_assets=[instrument],
                percentage=position_change,
                description=f"COT {direction} positioning change: {position_change:+.1f}% in {instrument}"
            )
            signals.append(signal)
        
        return signals
    
    def _calculate_magnitude(self, amount: float) -> FlowMagnitude:
        """Calculate flow magnitude based on amount."""
        if not self.thresholds or 'flow_thresholds' not in self.flows_config:
            # Default thresholds
            if amount >= 1_000_000_000:  # $1B+
                return FlowMagnitude.HIGH
            elif amount >= 500_000_000:  # $500M+
                return FlowMagnitude.MEDIUM
            else:
                return FlowMagnitude.LOW
        
        thresholds = self.flows_config['flow_thresholds']
        
        if amount >= thresholds.get('inflow_high', 1_000_000_000):
            return FlowMagnitude.HIGH
        elif amount >= thresholds.get('inflow_medium', 500_000_000):
            return FlowMagnitude.MEDIUM
        else:
            return FlowMagnitude.LOW
    
    def analyze_etf_flows(self) -> List[FlowSignal]:
        """
        Analyze ETF flows (placeholder for future implementation).
        
        Returns:
            List of ETF flow signals
        """
        # This would connect to actual ETF flow data sources
        logger.info("Analyzing ETF flows...")
        return []
    
    def analyze_cot_positioning(self) -> List[FlowSignal]:
        """
        Analyze COT positioning (placeholder for future implementation).
        
        Returns:
            List of COT flow signals
        """
        # This would connect to CFTC COT data
        logger.info("Analyzing COT positioning...")
        return []
    
    def detect_institutional_rotation(self, events: List[NormalizedEvent]) -> List[FlowSignal]:
        """
        Detect institutional rotation patterns.
        
        Args:
            events: List of events to analyze
            
        Returns:
            List of rotation signals
        """
        # Look for concurrent flows in opposite directions
        flow_events = [e for e in events if e.event_type == EventType.FLOW_SIGNAL]
        
        if len(flow_events) < 2:
            return []
        
        # Simplified rotation detection
        # In production, would analyze patterns of inflows/outflows across sectors
        
        return []
