# GIID - Global Institutional Intelligence Desk

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

## Overview

GIID (Global Institutional Intelligence Desk) is a comprehensive, production-ready institutional intelligence system that monitors global financial markets, regulations, geopolitics, ratings, capital flows, IPOs, FX, and precious metals. Designed for institutional investors and financial professionals who need actionable intelligence with verified sources and impact scoring.

## Key Features

✅ **Multi-Source Data Collection**
- Official sources (SEC, regulatory filings, PR wires)
- Rating agencies (Moody's, S&P, Fitch)
- Capital flows (ETF flows, COT data)
- FX and precious metals markets
- Geopolitical events and sanctions

✅ **Advanced Verification Engine**
- Tier-based source ranking (Tier 1-4)
- Cross-verification with multiple sources
- Confidence scoring (Low/Medium/High)
- Institutional signal detection

✅ **Intelligent Scoring System**
- 0-120 impact scoring scale
- Multi-factor analysis:
  - Source reliability (0-20)
  - Financial magnitude (0-25)
  - Project stage (0-15)
  - Regulatory severity (0-20)
  - Thesis relevance (0-20)
  - Institutional signal strength (0-20)

✅ **Automated Reporting**
- Daily intelligence briefs (Markdown format)
- Executive summaries (max 12 lines)
- Material events tracking (score ≥70)
- Deep-dive queue (score ≥80)
- Nothing material notifications

✅ **Capital Flows Analysis**
- ETF flow tracking
- COT (Commitments of Traders) positioning
- Institutional rotation detection
- Flow signal generation

## Installation

### Prerequisites
- Python 3.11+
- pip or uv package manager

### Quick Start

```bash
# Clone the repository
cd giid/

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .

# Run the system
python src/main.py
```

## Project Structure

```
giid/
├── config/                  # YAML configuration files
│   ├── watchlists.yaml     # Sectors, tickers, keywords
│   ├── institutions.yaml   # Tier-1 banks and sources
│   ├── ratings.yaml        # Rating agencies config
│   ├── flows.yaml          # ETF and COT settings
│   ├── fx_metals.yaml      # FX pairs and metals
│   ├── people.yaml         # Key decision makers
│   ├── geopolitics.yaml    # Chokepoints and regions
│   └── thresholds.yaml     # Scoring thresholds
├── src/
│   ├── collectors/         # Data collection modules
│   ├── verify/            # Verification engine
│   ├── normalize/         # Data normalization
│   ├── dedup/             # Deduplication & clustering
│   ├── score/             # Impact scoring
│   ├── flows/             # Capital flows analysis
│   ├── report/            # Report generation
│   └── main.py            # Main entry point
├── data/                   # Processed data storage
├── reports/                # Generated reports
├── tests/                  # Unit tests
├── requirements.txt
├── setup.py
├── README.md
└── PROMPT.md              # AI agent guidance
```

## Configuration

### Watchlists (config/watchlists.yaml)

Define sectors, tickers, and keywords to monitor:

```yaml
sectors:
  uranium:
    name: "Uranium"
    keywords:
      - "uranium mining"
      - "nuclear fuel"
    tickers:
      - "URA"
      - "URNM"
```

### Institutions (config/institutions.yaml)

Configure Tier-1 banks and institutional sources:

```yaml
tier_1_banks:
  - name: "Goldman Sachs"
    domains:
      - "goldmansachs.com"
    weight: 20
```

### Thresholds (config/thresholds.yaml)

Set scoring and alert thresholds:

```yaml
alert_levels:
  critical:
    threshold: 90
    action: "immediate_notification"
  high:
    threshold: 70
    action: "daily_report_top_section"
```

## Usage

### Running the System

```bash
# Run full GIID pipeline
python src/main.py

# Output:
# - Logs to console and giid.log
# - Events data to data/events_TIMESTAMP.json
# - Daily brief to reports/daily_brief_TIMESTAMP.md
```

### Sample Output

The system generates a comprehensive daily brief including:

1. **Executive Summary** (max 12 lines)
2. **Material Events Table** (Top-10, score ≥70)
3. **Institutional & Rating Signals**
4. **Capital Flows & IPOs**
5. **Geopolitics & Regulation**
6. **Deep-Dive Queue** (score ≥80)
7. **Nothing Material** section

### Example Report

```markdown
# GIID Daily Intelligence Brief
**Date**: 2024-01-13 14:30 UTC

## Executive Summary
**Top Event**: Moody's upgrades mining company (Impact: 92)
**Active Sectors**: Uranium (4), Energy (2), Critical Minerals (1)
**Material Events**: 8 events scored ≥70

## Material Events (Top-10)
| Score | Sector | Headline | Source |
|-------|--------|----------|--------|
| 92 | Uranium | Moody's upgrades... | Moody's |
| 88 | Energy | US Treasury sanctions... | Treasury |
...
```

## Testing

The GIID system includes comprehensive tests. However, due to the package structure, tests should be run after installing the package:

```bash
# Install in development mode
pip install -e .

# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/
```

### Quick Verification

To verify the system works without installing, simply run the main script:

```bash
# Run the full GIID pipeline
python src/main.py

# This will:
# 1. Collect events from all sources
# 2. Verify and score events
# 3. Generate a daily brief report
# 4. Save data to data/ and reports/ directories
```

Expected output:
- Daily brief report: `reports/daily_brief_TIMESTAMP.md`
- Events data: `data/events_TIMESTAMP.json`
- Log file: `giid.log`

## GitHub Actions Integration

The system includes a GitHub Actions workflow for automated daily reports:

```yaml
# .github/workflows/daily_report.yaml
name: Daily Intelligence Report
on:
  schedule:
    - cron: '0 6 * * *'  # 6 AM Jerusalem time
  workflow_dispatch:
```

## Architecture

### Data Flow

```
1. Collectors → Raw Events
2. Verification Engine → Verified Events (with confidence)
3. Normalizer → Normalized Events (standard schema)
4. Deduplicator → Unique Events
5. Scorer → Scored Events (0-120)
6. Flow Engine → Flow Signals
7. Report Generator → Daily Brief (Markdown)
```

### Verification Process

1. **Source Ranking**: Classify source as Tier 1-4
2. **Cross-Checking**: Verify against secondary sources
3. **Confidence Assignment**: Low/Medium/High based on:
   - Source tier
   - Number of confirmations
   - Cross-verification status

### Impact Scoring Components

```
Total Score (0-120) =
  + Source Reliability (0-20)
  + Financial Magnitude (0-25)
  + Project Stage (0-15)
  + Regulatory Severity (0-20)
  + Thesis Relevance (0-20)
  + Institutional Signal (0-20)
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or feature requests, please open a GitHub issue.

## Timezone

- Default timezone: **Asia/Jerusalem**
- All timestamps in UTC internally
- Reports display Jerusalem time

## Language Support

- **Code & Comments**: English
- **Reports**: Supports Hebrew and English
- **Configuration**: YAML (UTF-8)

---

**Built with ❤️ for institutional investors**
