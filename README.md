# 📊 Monday.com BI Agent

An AI-powered Business Intelligence system that transforms monday.com board data into actionable executive insights using weighted forecasting, quarter-based analytics, and multi-sector revenue analysis.

## ✨ Features

### 🎯 Core Intelligence
- **AI Query Parsing** - Convert business questions into structured intent with GPT-4o-mini
- **Weighted Revenue Forecasting** - Stage-based probability modeling for realistic pipeline forecasts
- **Quarter-Based Analytics** - Automatic Q1-Q4 classification and quarterly trend analysis
- **Cross-Board Analysis** - Correlate Deals board with Work Orders board
- **Multi-Sector Intelligence** - Revenue breakdown by industry/sector
- **Win Rate Calculation** - Track conversion and win metrics

### 📈 Advanced Analytics
- **Expected Revenue** - Weighted forecast based on deal stage conversion probabilities
- **Pipeline Health** - Data quality scoring (coverage %, missing values)
- **Trend Analysis** - Monthly and quarterly revenue trends
- **Bottleneck Detection** - Identify slow conversion stages
- **Risk Assessment** - Data-driven risk identification
- **Revenue Concentration** - Measure pipeline dependency

### 🤖 AI Integration
- **Natural Language Processing** - Ask questions in plain English
- **Founder-Grade Reports** - Leadership-ready BI insights with structured formatting
- **Anti-Hallucination Guards** - LLM forced to use only provided data
- **Fallback Demo Mode** - Works without OpenAI credits for testing

## 📋 Architecture

```
User Query
    ↓
Query Parser (agent.py) → Structured Intent (JSON)
    ↓
BI Engine (bi_engine.py) ← Data Fetch (data_fetcher.py)
    ↓                           ↑
Data Pipeline:              monday.com API
    - Clean (data_cleaner.py)
    - Parse (dataframe_parser.py)
    ↓
Analytics & Insights (bi_engine.py)
    ↓
Report Generator (insight_generator.py) → GPT-4o-mini
    ↓
Executive Report (Streamlit UI)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- monday.com account with API access
- OpenAI API key (with active credits)

### Installation

```bash
# Clone or navigate to project
cd c:\Users\basav\Desktop\Skylark\monday_bi_agent

# Install dependencies
pip install streamlit pandas requests openai

# Or use requirements.txt (create if needed)
pip install -r requirements.txt
```

### Configuration

1. **Update [config.py](config.py)**
   ```python
   MONDAY_API_KEY = "your-monday-api-key"
   OPENAI_API_KEY = "your-openai-api-key"
   DEALS_BOARD_ID = 5026563623
   WORK_ORDERS_BOARD_ID = 5026563580
   ```

2. **Get API Keys:**
   - Monday.com: https://monday.com/developers
   - OpenAI: https://platform.openai.com/api-keys

### Run the App

```bash
streamlit run app.py
```

App will be available at:
- Local: `http://localhost:8501`
- Network: `http://10.20.26.218:8501`

## 📝 Usage Examples

### Example Queries
```
"What's our total pipeline value?"
→ Returns weighted forecast + total pipeline

"Show me revenue by sector this quarter"
→ Breaks down revenue by industry with rankings

"What's our win rate?"
→ Calculates conversion rates from deals data

"Which deals are at risk?"
→ Identifies bottleneck stages and slow deals

"Give me a forecast for Q1"
→ Quarter-specific expected revenue analysis
```

## 🏗️ Project Structure

```
monday_bi_agent/
├── README.md                 # This file
├── config.py                 # API keys & board IDs
├── app.py                    # Streamlit UI entry point
├── agent.py                  # Query parser (NLP)
├── bi_engine.py              # Analytics engine (BI logic)
├── data_fetcher.py           # monday.com API integration
├── dataframe_parser.py       # JSON → DataFrame conversion
├── data_cleaner.py           # Data normalization & cleaning
├── insight_generator.py      # Report generation (LLM)
└── test_api.py              # API connectivity test
```

## 🔧 File Descriptions

### [agent.py](agent.py)
- Converts natural language queries to structured intent
- Extracts metrics: revenue, pipeline, forecast, sector, risk
- Auto-detects time ranges: this_quarter, this_month, this_year
- Temperature=0 for deterministic output
- Fallback demo response when OpenAI unavailable

### [bi_engine.py](bi_engine.py)
- Core business intelligence engine
- **Stage Probability Model:** Lead(10%) → Won(100%)
- **Quarter Logic:** Automatic Q1-Q4 classification
- **Expected Revenue:** Weighted by deal stage conversion probability
- **Column Detection:** Dynamically finds stage, amount, sector, date columns
- **Data Quality Scoring:** Calculates completeness percentage

### [insight_generator.py](insight_generator.py)
- Generates founder-level BI reports
- Structured output: Executive Summary, Revenue Intelligence, Pipeline Health, etc.
- Data validation before LLM processing
- Fallback demo response with realistic numbers
- Temperature=0.2 for consistent but slightly flexible output

### [data_fetcher.py](data_fetcher.py)
- Monday.com GraphQL integration
- Fetches items with column values
- Uses `items_page` API endpoint (current version)
- Handles pagination (limit: 100 items)

### [dataframe_parser.py](dataframe_parser.py)
- Converts monday.com JSON to Pandas DataFrame
- Error handling for API failures
- Column name normalization

### [data_cleaner.py](data_cleaner.py)
- Fills missing values ("Unknown")
- Text normalization (lowercase, strip)
- Date parsing and standardization

### [app.py](app.py)
- Streamlit UI
- Data caching for performance
- Query input → Report output pipeline
- Two-board data loading (Deals + Work Orders)

## 📊 BI Metrics Output

### Pipeline Analysis
```json
{
  "pipeline_by_stage": {
    "lead": 150000,
    "qualified": 325000,
    "proposal": 425000,
    "negotiation": 275000,
    "contract": 175000
  },
  "expected_revenue_weighted": 425000,
  "total_pipeline_value": 1350000,
  "deal_count": 48
}
```

### Revenue Breakdown
```json
{
  "sector_revenue": {
    "technology": 625000,
    "finance": 375000,
    "healthcare": 250000
  },
  "revenue_by_stage": {...}
}
```

### Data Quality
```json
{
  "data_quality": {
    "quality_score": 0.92,
    "missing_cells": 8,
    "records": 200
  }
}
```

## 🔐 Security

⚠️ **IMPORTANT:** Never commit API keys to version control!

### Best Practices
1. Use environment variables:
   ```bash
   $env:MONDAY_API_KEY = "your-key"
   $env:OPENAI_API_KEY = "your-key"
   ```

2. Add to `.gitignore`:
   ```
   config.py
   .env
   *.pyc
   __pycache__/
   ```

3. Use `.env` files:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
   ```

## 🐛 Troubleshooting

### Error: "Cannot query field 'items'"
- **Cause:** Old GraphQL query format
- **Fix:** Update [data_fetcher.py](data_fetcher.py) to use `items_page`

### Error: "api_key client option must be set"
- **Cause:** Missing OpenAI API key
- **Fix:** Set `OPENAI_API_KEY` in [config.py](config.py)

### Error: "insufficient_quota"
- **Cause:** OpenAI account out of credits
- **Fix:** Add payment method at https://platform.openai.com/account/billing
- **Workaround:** App uses demo mode fallback

### Error: "KeyError: 'stage'"
- **Cause:** monday.com board doesn't have stage/status column
- **Fix:** Update board IDs in [config.py](config.py) or rename columns in monday.com

### Slow data loading
- **Fix:** Data is cached with `@st.cache_data`
- Clear cache: Streamlit menu → Clear cache

## 🚦 Testing

### Quick API Test
```bash
python test_api.py
```
Verifies monday.com connectivity

### Manual Testing
1. Run `streamlit run app.py`
2. Try queries:
   - "What's our pipeline?"
   - "Show me this quarter's forecast"
   - "Revenue by sector?"

## 📈 Stage Probability Model

Used for weighted revenue forecasting:

| Stage | Probability | Example |
|-------|------------|---------|
| Lead | 10% | Early prospect, no engagement |
| Qualified | 30% | Showed interest, fit confirmed |
| Proposal | 50% | Proposal sent, negotiating |
| Negotiation | 70% | Terms being discussed |
| Contract | 85% | Legal review, close to signing |
| Won | 100% | Deal closed |
| Lost | 0% | Deal lost |

**Formula:** Expected Revenue = Sum(DealAmount × StageProbability)

## 🎯 Strategic Recommendations

The system generates founder-level insights including:
1. **Revenue Acceleration** - Which deals to prioritize
2. **Pipeline Health** - Bottleneck identification
3. **Risk Mitigation** - Concentration and data quality risks
4. **Sector Strategy** - Growth opportunities by industry
5. **Execution Priorities** - Data-driven action items

## 🔄 Quarterly Analysis

Automatic detection and analysis:
- Current quarter calculation (Q1-Q4)
- Quarter start/end dates
- Quarterly revenue trends
- Year-over-year comparisons
- Quarterly deal velocity

## 🤝 Contributing

To improve the BI Agent:

1. Enhance stage probability model in [bi_engine.py](bi_engine.py)
2. Add new metrics in analytics section
3. Improve LLM prompt in [insight_generator.py](insight_generator.py)
4. Add cross-board intelligence logic
5. Expand data quality checks

## 📚 API Documentation

### Monday.com GraphQL Query
```graphql
{
  boards(ids: BOARD_ID) {
    items_page(limit: 100) {
      items {
        name
        column_values {
          id
          text
        }
      }
    }
  }
}
```

### OpenAI Models Used
- `gpt-4o-mini` - Query parsing and report generation
- Temperature: 0 (deterministic query parsing), 0.2 (flexible reporting)

## 📊 Example Report Output

```
📊 Executive Summary:
- Expected revenue this quarter: $425,000 (weighted forecast)
- Total pipeline value: $1,250,000
- Deal count: 18 active deals
- Data confidence score: 92%

📈 Revenue Intelligence:
- Weighted forecast applies stage-based conversion probabilities
- Revenue concentration risk: 35% in top 3 deals

📊 Pipeline Health:
- Qualified: $425,000 (34%)
- Proposal: $380,000 (30%)
- Bottleneck: Proposal stage (45+ days avg)

🎯 Strategic Recommendations:
1. Close 5 Contract stage deals = $144,500 quick win
2. Accelerate Proposal stage to reduce 45-day cycle
3. Expand Healthcare sector (currently 20%, growth potential)
```

## 🎓 Learning Resources

- [Monday.com API Docs](https://developer.monday.com)
- [OpenAI API Guide](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas User Guide](https://pandas.pydata.org/docs)

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#-troubleshooting) section
2. Review logs in terminal
3. Verify API keys and board IDs in [config.py](config.py)
4. Test connectivity: `python test_api.py`

## 📄 License

This project is for internal use. Modify as needed for your organization.

---

**Last Updated:** February 11, 2026
**Version:** 1.0
**Status:** Production Ready ✅
