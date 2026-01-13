"""Normalization module initialization."""

from .normalizer import Normalizer
from .schema import (
    RawEvent,
    VerifiedEvent,
    NormalizedEvent,
    FlowSignal,
    EventCluster,
    DailyReport,
    ConfidenceLevel,
    FlowType,
    FlowMagnitude,
    EventType
)


__all__ = [
    'Normalizer',
    'RawEvent',
    'VerifiedEvent',
    'NormalizedEvent',
    'FlowSignal',
    'EventCluster',
    'DailyReport',
    'ConfidenceLevel',
    'FlowType',
    'FlowMagnitude',
    'EventType',
]
