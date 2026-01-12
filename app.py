import streamlit as st
import pandas as pd
import plotly.express as px
from pandasai import SmartDataframe

# --- UNIVERSAL IMPORT BLOCK ---
# We try to import OpenAI from all known locations.
# This fixes the "Critical Error" by finding the one that exists on your machine.
llm_class = None

# Attempt 1: The New Extension (pandasai-openai)
try:
    from pandasai_openai import OpenAI
    llm_class = OpenAI
except ImportError:
    pass

# Attempt 2: The Standard Library (pandasai.llm)
if llm_class is None:
    try:
        from pandasai.llm import OpenAI
        llm_class = OpenAI
    except ImportError:
        pass

# Attempt 3: The Submodule (pandasai.llm.openai)
if llm_class is None:
    try:
        from pandasai.llm.openai import OpenAI
        llm_class = OpenAI
    except ImportError:
        pass

# Final Check
if llm_class is None:
    st.error("❌ CRITICAL SETUP ERROR: The 'OpenAI' library cannot be found.")
    st.info("Please run this command in your terminal: pip install pandasai-openai")
    st.stop()

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Content Strategy Copilot", page_icon="🎬", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_master.csv')
        df_fin = pd.read_csv('processed_financials.csv')
        return df, df_fin
    except FileNotFoundError:
        st.error("❌ Data files not found! Make sure 'processed_master.csv' is in the folder.")
        return None, None

df_master, df_financials = load_data()

if df_master is None:
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("🎬 Strategy Copilot")
page = st.sidebar.radio("Navigate", ["📊 Executive Dashboard", "🤖 AI Analyst (Copilot)"])

# --- PAGE 1: DASHBOARD ---
if page == "📊 Executive Dashboard":
    st.title("📊 Executive Content Performance Dashboard")
    
    # 0. KPI ROW (Top of Page)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", f"{df_master['user_id'].nunique():,}")
    col2.metric("Total Watch Hours", f"{int(df_master['watch_duration_minutes'].sum()/60):,} hrs")
    col3.metric("Avg ROI", f"${df_financials['roi'].mean()/1e6:.1f}M")
    
    st.markdown("---")
    
    # 1. VIEWERSHIP VS RETENTION (First Chart)
    st.subheader("1. Viewership vs. Retention Analysis")
    q1_stats = df_master.groupby('title').agg({'session_id':'count', 'progress_percentage':'mean'}).reset_index()
    q1_stats.columns = ['title', 'views', 'retention']
    
    fig1 = px.scatter(
        q1_stats, 
        x='views', 
        y='retention', 
        color='retention', 
        title="Views vs Retention (The 'Clickbait' Check)", 
        hover_name='title',
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # 2. 4K DROP-OFF (Second Chart)
    st.subheader("2. Technical Friction Audit (4K Drop-off)")
    df_4k = df_master[df_master['quality'] == '4K']
    
    if not df_4k.empty:
        device_perf = df_4k.groupby('device_type')['progress_percentage'].mean().reset_index()
        fig2 = px.bar(
            device_perf, 
            x='device_type', 
            y='progress_percentage',
            title="Average Completion of 4K Content by Device",
            color='progress_percentage',
            range_y=[0, 100],
            labels={'progress_percentage': 'Completion %', 'device_type': 'Device'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No 4K data available for this analysis.")

    st.markdown("---")

    # 3. GLOBAL MAP (Third Chart)
    st.subheader("3. Global Market Penetration")
    country_counts = df_master['location_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Sessions']
    
    fig3 = px.choropleth(
        country_counts,
        locations='Country',
        locationmode='country names',
        color='Sessions',
        title="User Activity Heatmap",
        color_continuous_scale='Plasma'
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Visuals
    st.subheader("1. Viewership vs. Retention Analysis")
    q1_stats = df_master.groupby('title').agg({'session_id':'count', 'progress_percentage':'mean'}).reset_index()
    fig = px.scatter(q1_stats, x='session_id', y='progress_percentage', color='progress_percentage', title="Views vs Retention", hover_name='title')
    st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: AI COPILOT ---
elif page == "🤖 AI Analyst (Copilot)":
    st.title("🤖 AI Strategy Consultant")
    st.markdown("Ask questions like: *'Which genre has the highest ROI?'* or *'Top 5 movies by watch time'*")
    
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    
    if not api_key:
        st.warning("⚠️ Enter your API Key in the sidebar to start.")
    else:
        try:
            # Initialize the LLM using the class we found earlier
            llm = llm_class(api_token=api_key)
            
            sdf = SmartDataframe(
                df_master,
                config={"llm": llm, "verbose": True}
            )
            
            user_query = st.text_area("Ask your question:", height=100)
            
            if st.button("Generate Insight"):
                if user_query:
                    with st.spinner("Analyzing..."):
                        response = sdf.chat(user_query)
                        st.success("Analysis Complete")
                        st.write(response)
                else:
                    st.warning("Please type a question.")
                    
        except Exception as e:
            st.error(f"Error: {e}")