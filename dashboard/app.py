import streamlit as st
import json
import pandas as pd
import os
import subprocess
from datetime import datetime

st.set_page_config(page_title="PIVX Outreach Command Center", layout="wide", page_icon="🛡️")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ PIVX Outreach Command Center")

# --- Sidebar: Control Panel ---
with st.sidebar:
    st.header("Controls")
    st.info("Click below to trigger the AI Workforce. This will scrape GitHub, score repos, and draft PIVX proposals.")
    
    if st.button("🚀 Run Full Pipeline", use_container_width=True):
        with st.status("Executing PIVX Outreach Sequence...", expanded=True) as status:
            st.write("🔍 Scraping GitHub...")
            subprocess.run(["python", "scripts/scraper.py"])
            
            st.write("⚖️ Scoring Repositories...")
            subprocess.run(["python", "scripts/scorer.py"])
            
            st.write("✍️ AI Drafting (Gemini 3)...")
            subprocess.run(["python", "scripts/drafter.py"])
            
            st.write("💾 Logging Results...")
            subprocess.run(["python", "scripts/logger.py"])
            
            status.update(label="✅ Pipeline Complete!", state="complete", expanded=False)
        st.balloons()

# --- Data Loading ---
log_file = 'data/outreach_log.json'

if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        data = json.load(f)
    
    if data:
        df = pd.DataFrame(data)

        # Dashboard Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Leads", len(df))
        m2.metric("Top Score", f"{df['final_score'].max()}%")
        m3.metric("Avg Quality", f"{round(df['final_score'].mean(), 1)}%")
        m4.metric("Last Updated", df['logged_at'].iloc[-1].split()[0] if 'logged_at' in df else "N/A")

        st.divider()

        # Tabs
        tab1, tab2, tab3 = st.tabs(["🎯 Priority Leads", "📨 Proposal Editor", "📈 Growth Stats"])

        with tab1:
            st.dataframe(
                df.sort_values(by='final_score', ascending=False),
                column_config={
                    "url": st.column_config.LinkColumn("GitHub Repo"),
                    "final_score": st.column_config.ProgressColumn("Priority", min_value=0, max_value=100, format="%d%%"),
                    "stars": st.column_config.NumberColumn("Stars", format="%d ⭐")
                },
                hide_index=True,
                use_container_width=True
            )

        with tab2:
            selected = st.selectbox("Select Project", df['name'].unique())
            row = df[df['name'] == selected].iloc[0]
            
            st.subheader(f"Proposal for {selected}")
            # Editable text area so you can tweak the AI draft
            final_pitch = st.text_area("Edit Draft:", value=row['proposal_draft'], height=350)
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button(f"Go to {selected}", row['url'])
            with c2:
                if st.button("Mark as Contacted"):
                    st.success("Moved to contacted list!")

        with tab3:
            st.bar_chart(df.set_index('name')['stars'])
            st.write("Current Keywords targeted: *Privacy, ZK, zk-SNARKs, Payments*")

    else:
        st.info("Log is empty. Click 'Run Full Pipeline' in the sidebar.")