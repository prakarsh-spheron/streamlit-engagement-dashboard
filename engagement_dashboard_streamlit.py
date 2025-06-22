
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

st.set_page_config(layout="wide")
st.title("📊 Engagement Dashboard")

# Upload Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Projects")

    # Clean dates
    df['First Reachout Date'] = pd.to_datetime(df['First Reachout Date'], errors='coerce')
    df['Last Reachout Date'] = pd.to_datetime(df['Last Reachout Date'], errors='coerce')

    st.header("📈 Engagement Timeline per Project")
    df_timeline = df.dropna(subset=['First Reachout Date', 'Last Reachout Date', 'Engagement Stage'])
    fig_timeline = px.timeline(
        df_timeline,
        x_start="First Reachout Date",
        x_end="Last Reachout Date",
        y="Company Name",
        color="Engagement Stage",
        hover_data=["Engagement Stage"]
    )
    fig_timeline.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_timeline, use_container_width=True)

    # Daily new reachouts
    st.header("📅 Daily New Reachouts")
    daily_counts = df['First Reachout Date'].dropna().dt.date.value_counts().sort_index()
    daily_df = daily_counts.reset_index()
    daily_df.columns = ['Date', 'New Reachouts']
    fig_daily = px.line(daily_df, x='Date', y='New Reachouts', markers=True)
    st.plotly_chart(fig_daily, use_container_width=True)

    # Weekly announced (Engagement Stage = Announced)
    st.header("📆 Weekly Reach Out Announced")
    announced_df = df[df['Engagement Stage'] == 'Announced']
    weekly_announce = announced_df['First Reachout Date'].dropna().dt.to_period('W').value_counts().sort_index()
    weekly_announce_df = weekly_announce.reset_index()
    weekly_announce_df.columns = ['Week', 'Reach Out Announced']
    weekly_announce_df['Week'] = weekly_announce_df['Week'].astype(str)
    fig_announce = px.line(weekly_announce_df, x='Week', y='Reach Out Announced', markers=True)
    st.plotly_chart(fig_announce, use_container_width=True)

    # Weekly partnerships (Connection Stage = Synergy Finalised)
    st.header("🤝 Weekly Partnerships Announced")
    partners_df = df[df['Connection Stage'] == 'Synergy Finalised']
    weekly_partners = partners_df['First Reachout Date'].dropna().dt.to_period('W').value_counts().sort_index()
    weekly_partners_df = weekly_partners.reset_index()
    weekly_partners_df.columns = ['Week', 'Partnerships Announced']
    weekly_partners_df['Week'] = weekly_partners_df['Week'].astype(str)
    fig_partners = px.line(weekly_partners_df, x='Week', y='Partnerships Announced', markers=True)
    st.plotly_chart(fig_partners, use_container_width=True)
