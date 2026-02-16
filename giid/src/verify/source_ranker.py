"""Source ranking for verification engine."""

from typing import Dict, List
import logging
import yaml
from pathlib import Path


logger = logging.getLogger(__name__)


class SourceRanker:
    """Ranks sources by tier and reliability."""
    
    # Tier 1 sources (highest reliability)
    TIER_1_SOURCES = [
        "sec.gov",
        "moodys.com",
        "spglobal.com",
        "fitchratings.com",
        "federalreserve.gov",
        "ecb.europa.eu",
        "bankofengland.co.uk",
        "treasury.gov",
        "cftc.gov"
    ]
    
    # Tier 2 sources (reliable institutional)
    TIER_2_SOURCES = [
        "goldmansachs.com",
        "gs.com",
        "jpmorgan.com",
        "morganstanley.com",
        "ubs.com",
        "citigroup.com",
        "citi.com",
        "bankofamerica.com",
        "bofa.com",
        "db.com",
        "deutschebank.com",
        "bloomberg.com",
        "reuters.com",
        "ft.com"
    ]
    
    # Tier 3 sources (standard news)
    TIER_3_SOURCES = [
        "prnewswire.com",
        "businesswire.com",
        "globenewswire.com",
        "wsj.com",
        "cnbc.com",
        "marketwatch.com"
    ]
    
    def __init__(self, config_path: str = None):
        """
        Initialize source ranker.
        
        Args:
            config_path: Path to institutions config file
        """
        self.tier_map = {}
        self._load_config(config_path)
        self._build_tier_map()
    
    def _load_config(self, config_path: str):
        """Load institutions configuration."""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    self.config = yaml.safe_load(f)
            except Exception as e:
                logger.warning(f"Failed to load config: {e}")
                self.config = {}
        else:
            self.config = {}
    
    def _build_tier_map(self):
        """Build mapping of domains to tier levels."""
        for domain in self.TIER_1_SOURCES:
            self.tier_map[domain] = 1
        
        for domain in self.TIER_2_SOURCES:
            self.tier_map[domain] = 2
        
        for domain in self.TIER_3_SOURCES:
            self.tier_map[domain] = 3
    
    def rank(self, source: str) -> int:
        """
        Rank a source URL/domain.
        
        Args:
            source: Source URL or domain
            
        Returns:
            Tier level (1=highest, 4=unverified)
        """
        if not source:
            return 4
        
        source_lower = source.lower()
        
        # Check each tier
        for domain, tier in self.tier_map.items():
            if domain in source_lower:
                return tier
        
        # Unknown source
        return 4
    
    def is_tier_1(self, source: str) -> bool:
        """Check if source is Tier 1."""
        return self.rank(source) == 1
    
    def is_institutional(self, source: str) -> bool:
        """Check if source is institutional (Tier 1 or 2)."""
        return self.rank(source) <= 2
    
    def get_source_weight(self, source: str) -> int:
        """
        Get reliability weight for source.
        
        Args:
            source: Source URL or domain
            
        Returns:
            Reliability weight (0-25)
        """
        tier = self.rank(source)
        weights = {
            1: 25,  # Tier 1: Official/regulatory
            2: 20,  # Tier 2: Major institutions
            3: 15,  # Tier 3: Reputable news
            4: 5    # Tier 4: Unverified
        }
        return weights.get(tier, 5)
