# Financial Markets Key Figures Intelligence Agent
### סוכן אוטונומי לאיסוף מידע על דמויות מפתח המשפיעות על שוק ההון

An autonomous agent that monitors and analyzes key financial figures influencing capital markets, including central bank officials, regulators, investors, CEOs, and Israeli financial leaders.

## Features

- **Comprehensive Database**: Tracks 47+ key financial figures across 8 categories
- **Real-time Analysis**: AI-powered market influence analysis (with OpenAI API)
- **Market Intelligence**: Generates briefings and reports on market movers
- **Israeli Focus**: Special attention to Israeli financial market figures
- **Demo Mode**: Works without API keys for demonstration

## Key Figure Categories

### 🏛️ Central Banks (בנקים מרכזיים)
- Jerome Powell (Fed Chairman)
- Christine Lagarde (ECB President) 
- Andrew Bailey (BoE Governor)
- Kazuo Ueda (BoJ Governor)

### ⚖️ Regulators (רגולטורים)
- Gary Gensler (SEC Chairman)
- Rostin Behnam (CFTC Chairman)
- Janet Yellen (Treasury Secretary)
- Lina Khan (FTC Chairwoman)

### 💼 Investors & Asset Managers (משקיעים ומנהלי נכסים)
- Warren Buffett (Berkshire Hathaway)
- Larry Fink (BlackRock)
- Ray Dalio (Bridgewater)
- Ken Griffin (Citadel)
- Bill Ackman (Pershing Square)
- Cathie Wood (ARK Invest)
- Michael Burry (Scion)
- And more...

### 🏦 Banking Executives (בנקים)
- Jamie Dimon (JPMorgan)
- Brian Moynihan (Bank of America)
- David Solomon (Goldman Sachs)
- Jane Fraser (Citi)

### 💻 Tech CEOs (מנכ״לי טכנולוgia)
- Jensen Huang (NVIDIA)
- Lisa Su (AMD)
- Pat Gelsinger (Intel)
- Sundar Pichai (Alphabet)
- Satya Nadella (Microsoft)
- Tim Cook (Apple)
- Mark Zuckerberg (Meta)
- Andy Jassy (Amazon)
- Elon Musk (Tesla/SpaceX)
- Sam Altman (OpenAI)

### 🇮🇱 Israeli Key Figures (דמויות מפתח ישראליות)
- Prime Minister (ראש הממשלה)
- Finance Minister (שר האוצר)
- Defense Minister (שר הביטחון)
- Bank of Israel Governor (נגיד בנק ישראל)
- ISA Chairman (יו״ר רשות ניירות ערך)
- Major Banks CEOs (מנכ״לי בנקים גדולים)
- Defense Companies CEOs (מנכ״לי חברות ביטחוניות)
- TASE CEO (מנכ״ל הבורסה בת״א)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

For full AI analysis capabilities, set your OpenAI API key:

```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Usage

### Basic Usage (with OpenAI API)
```bash
python main.py
```

### Demo Mode (no API key needed)
```bash
python demo.py
```

## Example Output

```
🏦 Financial Markets Key Figures Intelligence Agent
============================================================

📊 Monitoring 47 key financial figures
📋 Categories available: central_banks, regulators, investors_asset_managers, banking_executives, tech_ceos, industry_energy, media_analysts, israel_key_figures

🔍 Example Analysis - Jerome Powell:
----------------------------------------
📊 Current Market Influence: VERY HIGH
As Fed Chairman, Powell's statements have immediate impact on:
• Interest rates and bond markets
• Dollar strength/weakness  
• Stock market valuations
• Inflation expectations
```

## API Reference

### Core Methods

- `get_figure_info(name, category=None)` - Get detailed information about a figure
- `list_figures_by_category(category)` - List all figures in a category
- `analyze_market_influence(name, news=None)` - AI analysis of market impact
- `generate_market_update_report(category=None)` - Comprehensive briefing report

### Categories
- `central_banks` - Central bank officials
- `regulators` - Financial regulators
- `investors_asset_managers` - Investment professionals
- `banking_executives` - Banking leaders
- `tech_ceos` - Technology company CEOs
- `industry_energy` - Industrial and energy leaders
- `media_analysts` - Media personalities and analysts
- `israel_key_figures` - Israeli financial market figures

## Contributing

Contributions are welcome! Please feel free to submit pull requests to add new figures, update information, or enhance functionality.

## License

MIT License - see LICENSE file for details.
