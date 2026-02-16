"""Deduplication module initialization."""

from .deduplicator import Deduplicator
from .clusterer import Clusterer


__all__ = [
    'Deduplicator',
    'Clusterer',
]
