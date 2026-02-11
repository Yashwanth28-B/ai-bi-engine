import pandas as pd
from datetime import datetime

# -------------------------------
# Stage probability model
# -------------------------------
STAGE_PROBABILITY = {
    "lead": 0.1,
    "qualified": 0.3,
    "proposal": 0.5,
    "negotiation": 0.7,
    "contract": 0.85,
    "won": 1.0,
    "lost": 0.0
}

# -------------------------------
# Time utilities
# -------------------------------
def get_quarter(date):
    return (date.month - 1) // 3 + 1

def get_current_quarter_range():
    now = pd.Timestamp.now()
    q = get_quarter(now)
    start_month = (q - 1) * 3 + 1
    start = pd.Timestamp(year=now.year, month=start_month, day=1)
    end = start + pd.DateOffset(months=3)
    return start, end

# -------------------------------
# BI ENGINE
# -------------------------------
def analyze(intent, deals_df, work_df):
    insights = {}

    # -------------------------------
    # Column detection
    # -------------------------------
    def find_col(df, keywords):
        for col in df.columns:
            for k in keywords:
                if k in col.lower():
                    return col
        return None

    amount_col = find_col(deals_df, ["amount", "value", "revenue"])
    stage_col = find_col(deals_df, ["stage", "status"])
    sector_col = find_col(deals_df, ["sector", "industry"])
    date_col   = find_col(deals_df, ["close_date", "date", "closing"])

    # -------------------------------
    # Data cleaning
    # -------------------------------
    if date_col:
        deals_df[date_col] = pd.to_datetime(deals_df[date_col], errors="coerce")

    if amount_col:
        deals_df[amount_col] = pd.to_numeric(deals_df[amount_col], errors="coerce").fillna(0)

    if stage_col:
        deals_df[stage_col] = deals_df[stage_col].astype(str).str.lower().str.strip()

    if sector_col:
        deals_df[sector_col] = deals_df[sector_col].astype(str).str.lower().str.strip()

    # -------------------------------
    # Time filtering (THIS QUARTER)
    # -------------------------------
    q_start, q_end = get_current_quarter_range()

    if date_col:
        q_deals = deals_df[
            (deals_df[date_col] >= q_start) &
            (deals_df[date_col] < q_end)
        ]
    else:
        q_deals = deals_df.copy()

    # -------------------------------
    # Expected revenue (weighted)
    # -------------------------------
    expected_revenue = 0
    weighted_rows = []

    if stage_col and amount_col:
        for _, row in q_deals.iterrows():
            stage = row[stage_col]
            amount = row[amount_col]

            prob = STAGE_PROBABILITY.get(stage, 0.25)
            weighted_value = amount * prob
            expected_revenue += weighted_value

            weighted_rows.append({
                "stage": stage,
                "amount": amount,
                "probability": prob,
                "expected_value": weighted_value
            })

    # -------------------------------
    # Pipeline aggregation
    # -------------------------------
    pipeline_by_stage = {}
    if stage_col and amount_col:
        pipeline_by_stage = q_deals.groupby(stage_col)[amount_col].sum().to_dict()

    # -------------------------------
    # Sector revenue
    # -------------------------------
    sector_revenue = {}
    if sector_col and amount_col:
        sector_revenue = q_deals.groupby(sector_col)[amount_col].sum().to_dict()

    # -------------------------------
    # Cross-board correlation (Deals ↔ Work Orders)
    # -------------------------------
    cross_board = {}
    work_sector_col = find_col(work_df, ["sector", "industry"])
    work_amount_col = find_col(work_df, ["amount", "value", "revenue"])
    
    if work_sector_col and work_amount_col:
        try:
            work_sector_rev = work_df.groupby(work_sector_col)[work_amount_col].sum().to_dict()
            cross_board = {
                "sales_pipeline_by_sector": sector_revenue,
                "execution_revenue_by_sector": work_sector_rev
            }
        except Exception as e:
            print(f"Cross-board analysis error: {e}")

    # -------------------------------
    # Data quality scoring
    # -------------------------------
    total_cells = deals_df.shape[0] * deals_df.shape[1]
    missing_cells = deals_df.isnull().sum().sum()
    quality_score = round(1 - (missing_cells / total_cells), 2) if total_cells else 0

    # -------------------------------
    # Output BI metrics (with intent filtering)
    # -------------------------------
    total_pipeline = 0
    if amount_col:
        try:
            total_pipeline = float(q_deals[amount_col].sum())
        except:
            total_pipeline = 0
    
    # Filter by intent metrics
    filtered_insights = {}
    if "pipeline" in intent.get("metrics", []):
        filtered_insights["pipeline_by_stage"] = pipeline_by_stage
    if "revenue" in intent.get("metrics", []) or "pipeline" in intent.get("metrics", []):
        filtered_insights["total_pipeline_value"] = total_pipeline
        filtered_insights["expected_revenue_weighted"] = round(expected_revenue, 2)
    if intent.get("sector"):
        filtered_insights["sector_revenue"] = sector_revenue
    
    insights = {
        "time_range": {
            "quarter_start": str(q_start.date()),
            "quarter_end": str(q_end.date())
        },
        "expected_revenue_weighted": round(expected_revenue, 2),
        "total_pipeline_value": total_pipeline,
        "deal_count": int(len(q_deals)),
        "pipeline_by_stage": pipeline_by_stage,
        "sector_revenue": sector_revenue,
        "weighted_pipeline_rows": weighted_rows[:10],  # sample for explainability
        "cross_board_intelligence": cross_board,
        "data_quality": {
            "missing_cells": int(missing_cells),
            "quality_score": quality_score,
            "records": len(deals_df)
        },
        "intent_used": {
            "metrics": intent.get("metrics", []),
            "sector": intent.get("sector", ""),
            "time_range": intent.get("time_range", "")
        }
    }

    return insights
