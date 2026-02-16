"""Data schemas for the GIID system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence level for verified events."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FlowType(str, Enum):
    """Types of capital flow signals."""
    EQUITY_INFLOW = "equity_inflow"
    EQUITY_OUTFLOW = "equity_outflow"
    BOND_INFLOW = "bond_inflow"
    BOND_OUTFLOW = "bond_outflow"
    RISK_OFF = "risk_off"
    RISK_ON = "risk_on"
    ROTATION = "rotation"


class FlowMagnitude(str, Enum):
    """Magnitude of capital flows."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EventType(str, Enum):
    """Types of events tracked by the system."""
    MERGER_ACQUISITION = "merger_acquisition"
    REGULATORY_APPROVAL = "regulatory_approval"
    LICENSE_GRANT = "license_grant"
    SANCTIONS = "sanctions"
    RATING_CHANGE = "rating_change"
    IPO_ANNOUNCEMENT = "ipo_announcement"
    DEBT_ISSUANCE = "debt_issuance"
    FACILITY_CLOSURE = "facility_closure"
    PRODUCTION_HALT = "production_halt"
    GEOPOLITICAL_EVENT = "geopolitical_event"
    FLOW_SIGNAL = "flow_signal"
    FX_EVENT = "fx_event"
    METALS_EVENT = "metals_event"
    INSTITUTIONAL_CALL = "institutional_call"


@dataclass
class RawEvent:
    """Raw event data from collectors."""
    id: str
    timestamp: datetime
    source: str
    url: Optional[str]
    headline: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlowSignal:
    """Capital flow signal data."""
    type: FlowType
    magnitude: FlowMagnitude
    linked_assets: List[str]
    amount: Optional[float] = None
    percentage: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    description: str = ""


@dataclass
class VerifiedEvent:
    """Event after verification process."""
    raw_event: RawEvent
    confidence: ConfidenceLevel
    source_tier: int
    verification_notes: str
    cross_checked: bool
    num_confirmations: int


@dataclass
class NormalizedEvent:
    """Normalized event with full metadata and scoring."""
    id: str
    timestamp: datetime
    event_type: EventType
    sector: str
    headline: str
    summary: str
    source: str
    source_tier: int
    confidence: ConfidenceLevel
    institutional_source: Optional[str] = None
    flow_signal: Optional[FlowSignal] = None
    impact_score: int = 0
    linked_assets: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    region: Optional[str] = None
    people_mentioned: List[str] = field(default_factory=list)


@dataclass
class EventCluster:
    """Cluster of related events."""
    cluster_id: str
    primary_event: NormalizedEvent
    related_events: List[NormalizedEvent]
    cluster_summary: str
    max_impact_score: int
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DailyReport:
    """Daily intelligence report data."""
    report_date: datetime
    executive_summary: str
    material_events: List[NormalizedEvent]
    flow_signals: List[FlowSignal]
    rating_actions: List[NormalizedEvent]
    institutional_calls: List[NormalizedEvent]
    geopolitical_events: List[NormalizedEvent]
    deep_dive_queue: List[NormalizedEvent]
    nothing_material: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
