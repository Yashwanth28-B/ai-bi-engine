import streamlit as st

from config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID
from data_fetcher import get_board_data
from dataframe_parser import monday_json_to_df
from data_cleaner import clean_data
from agent import interpret_query
from bi_engine import analyze
from insight_generator import generate_insight

# -------------------------------
# Load data from monday.com
# -------------------------------
@st.cache_data(show_spinner=True)
def load_data():
    # Fetch raw JSON
    deals_raw = get_board_data(DEALS_BOARD_ID)
    work_raw = get_board_data(WORK_ORDERS_BOARD_ID)

    # Convert to DataFrames
    deals_df = monday_json_to_df(deals_raw)
    work_df = monday_json_to_df(work_raw)

    # Clean data
    deals_df = clean_data(deals_df)
    work_df = clean_data(work_df)

    return deals_df, work_df

deals_df, work_df = load_data()

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📊 Monday.com BI Agent")

st.caption("AI-powered business intelligence over monday.com boards")

query = st.text_input("Ask your business question:")

if query:
    with st.spinner("Analyzing business data..."):
        intent = interpret_query(query)
        insights = analyze(intent, deals_df, work_df)
        response = generate_insight(insights)

    st.subheader("📈 Business Insights")
    st.markdown(response)
