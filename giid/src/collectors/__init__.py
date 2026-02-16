"""Collector module initialization."""

from .base_collector import BaseCollector
from .news_collector import NewsCollector
from .regulatory_collector import RegulatoryCollector
from .ratings_collector import RatingsCollector
from .flows_collector import FlowsCollector
from .fx_metals_collector import FXMetalsCollector


__all__ = [
    'BaseCollector',
    'NewsCollector',
    'RegulatoryCollector',
    'RatingsCollector',
    'FlowsCollector',
    'FXMetalsCollector',
]
