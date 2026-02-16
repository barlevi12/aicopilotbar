# GIID System - AI Agent Guidance (PROMPT.md)

## System Overview

GIID (Global Institutional Intelligence Desk) is a production-ready intelligence system for monitoring global financial markets with emphasis on:
- **Verification**: Only Tier-1/2 sources are trusted
- **Impact Scoring**: 0-120 scale, material threshold at ≥70
- **Actionability**: Reports focus on tradeable intelligence, not noise

## Core Principles

### 1. Source Verification (CRITICAL)
**Rule**: Never report unverified information.

**Tier System**:
- **Tier 1** (Official): SEC, Moody's, S&P, Fitch, Fed, ECB, Treasury, CFTC
- **Tier 2** (Institutional): Goldman Sachs, JPMorgan, Bloomberg, Reuters
- **Tier 3** (News): PR wires, WSJ, FT
- **Tier 4** (Unverified): Social media, blogs, rumors → REJECT

**Verification Process**:
1. Check if source is Tier-1 or Tier-2
2. If Tier-3 or below, require cross-confirmation from Tier-1/2
3. Assign confidence level based on verification
4. Include verification notes in output

### 2. Impact Scoring Formula

```
Total Score (0-120) = 
  Source Reliability (0-20)
  + Financial Magnitude (0-25)
  + Project Stage (0-15)
  + Regulatory Severity (0-20)
  + Thesis Relevance (0-20)
  + Institutional Signal (0-20)
```

**Scoring Guidelines**:
- **90+**: CRITICAL - Immediate alert required
- **70-89**: HIGH - Include in top section of daily brief
- **50-69**: MEDIUM - Include in standard section
- **<50**: LOW - Archive only, do not report

### 3. Institutional Signals (High Value)

**Priority Signals**:
1. **Rating Actions** (18-20 points):
   - Upgrades/downgrades from Moody's, S&P, Fitch
   - Outlook changes
   - Watch list additions
   
2. **Tier-1 Bank Sector Calls** (14-18 points):
   - Overweight/underweight sector calls
   - Price target changes
   - Initiation of coverage
   
3. **Thematic Macro Notes** (10-14 points):
   - Fed/ECB policy shifts
   - Geopolitical analysis from major institutions
   - Cross-asset flow analysis

### 4. Investment Thesis Focus

**Priority Sectors** (20 points for direct match):
- Uranium / Nuclear
- Critical Minerals (Lithium, Rare Earths, Copper)
- Energy (Oil, Gas, LNG)
- Satellites & Space Infrastructure
- Financials (for credit/flow insights)

**Keywords to Prioritize**:
- "uranium", "nuclear fuel", "enrichment"
- "lithium", "rare earth", "critical minerals"
- "sanctions", "export controls", "license"
- "rating upgrade", "outlook positive"
- "inflow", "positioning", "rotation"

### 5. Capital Flows Analysis

**Flow Types**:
- **Equity Inflow/Outflow**: ETF flow data
- **Risk-On/Risk-Off**: COT positioning shifts
- **Rotation**: Concurrent sector flows

**Magnitude Classification**:
- **HIGH**: $1B+ or 10%+ of AUM
- **MEDIUM**: $500M-$1B or 5-10% of AUM
- **LOW**: $100M-$500M or 2-5% of AUM

**Linked Assets**:
- Always connect flows to specific tickers/assets
- Track cross-asset correlations (e.g., USD strength → EM FX weakness)

### 6. Geopolitical Events

**Strategic Chokepoints** (High Priority):
- Strait of Hormuz (20% global oil)
- Suez Canal (12% global trade)
- Bab el-Mandeb / Red Sea
- Strait of Malacca
- Turkish Straits

**Event Types**:
- Sanctions announcements (OFAC, EU)
- Export controls (BIS, Commerce Dept)
- Chokepoint disruptions
- Strategic resource disputes

**Impact Assessment**:
- Direct: Affects specific asset class
- Indirect: Ripple effects (e.g., Red Sea → Europe shipping costs)
- Duration: Temporary vs. structural

### 7. Report Generation Rules

**Executive Summary** (Max 12 Lines):
1. Date & key highlight
2. Top event (highest score)
3. Active sectors breakdown
4. Flow summary (if material)
5. Geopolitical context (if relevant)
6. Material events count

**Material Events Table**:
- Top-10 events with score ≥70
- Columns: Score | Sector | Headline | Source
- Sort by impact score descending

**Deep-Dive Queue**:
- Events with score ≥80
- Indicate they require further analysis
- Max 5 events

**Nothing Material**:
- List sectors with NO events ≥70
- Useful negative information

### 8. Data Quality Standards

**Required Fields**:
- Every event must have: ID, timestamp, source, headline, sector
- Source tier must be determined
- Confidence level must be assigned

**Deduplication**:
- Events within 24h with 85%+ similarity = duplicate
- Keep highest-scored version
- Note in metadata if consolidated

**Clustering**:
- Events with 70%+ similarity = related cluster
- Group by sector and theme
- Useful for connected developments

### 9. Timezone & Language

**Timezone**:
- Default: Asia/Jerusalem (UTC+2/+3)
- Internal storage: UTC
- Report display: Jerusalem time

**Language**:
- Code/logs: English
- Reports: Can generate in Hebrew or English
- Use UTF-8 encoding throughout

### 10. Error Handling

**Collector Failures**:
- Retry up to 3 times with exponential backoff
- Log failures but continue with other sources
- Never fail entire pipeline due to one collector

**Data Validation**:
- Reject events with missing critical fields
- Log rejected events for review
- Continue processing valid events

**Verification Failures**:
- If source cannot be verified → confidence = LOW
- If no cross-confirmation available → note in report
- Never silently drop events

## AI Agent Instructions

When processing GIID tasks:

1. **Always verify sources first** - Check tier level before scoring
2. **Prioritize institutional signals** - Rating actions and bank calls are high-value
3. **Focus on actionable intelligence** - Skip low-score events
4. **Connect the dots** - Link related events (flows + ratings + geopolitics)
5. **Be concise** - Executive summary must fit in 12 lines
6. **Flag high-impact events** - Score ≥90 requires immediate attention
7. **Track "nothing material"** - Absence of news is also information
8. **Maintain timezone consistency** - UTC internally, Jerusalem for reports
9. **Log everything** - Comprehensive logs for auditability
10. **Never hallucinate** - Only report verified information with sources

## Sample Workflow

```python
# 1. Collect
raw_events = await collect_all_sources()

# 2. Verify
verified_events = verify_with_tier_check(raw_events)

# 3. Normalize
normalized_events = normalize_to_schema(verified_events)

# 4. Dedupe
unique_events = deduplicate(normalized_events)

# 5. Score
for event in unique_events:
    event.impact_score = calculate_impact(event)

# 6. Analyze Flows
flow_signals = analyze_capital_flows(unique_events)

# 7. Generate Report
daily_brief = generate_report(
    events=[e for e in unique_events if e.impact_score >= 70],
    flows=flow_signals
)
```

## Quality Checklist

Before generating final report, verify:

- [ ] All sources are Tier-1 or Tier-2 (or Tier-3 with confirmation)
- [ ] Impact scores calculated for all events
- [ ] Material events (≥70) identified
- [ ] Deep-dive queue (≥80) populated
- [ ] Flow signals analyzed and linked to assets
- [ ] Executive summary ≤12 lines
- [ ] Nothing material section included
- [ ] Report in proper Markdown format
- [ ] Timestamps in correct timezone
- [ ] All links and sources cited

## Advanced Features

### Cross-Asset Correlation
- Gold up + USD down + EM FX stable → Risk-off in DM only
- Oil sanctions + freight rates up → Supply chain impact
- Uranium upgrade + ETF inflow → Validation of thesis

### People Tracking
- Track statements from: Powell, Lagarde, Dimon, Yellen
- Weight their statements: Central bankers > CEOs > Analysts
- Monitor for policy shifts and sentiment changes

### Institutional Rotation Detection
- Watch for concurrent sector flows
- Example: Tech outflow + Energy inflow = Rotation to value
- Flag when 3+ concurrent signals within 5 days

---

**Remember**: Quality over quantity. One high-confidence, high-impact event is worth more than 100 unverified rumors.
