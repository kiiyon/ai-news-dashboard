import streamlit as st
import feedparser
import datetime
from dateutil import parser
import time

# --- Page Config ---
st.set_page_config(
    page_title="AI News Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Rich & Modern Design ---
st.markdown(
    """
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Rajdhani:wght@600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Background */
    .stApp {
        background-color: #0e1117;
    }

    /* Header Styling - Cooler English Title */
    .main-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-shadow: 0 0 20px rgba(0, 114, 255, 0.3);
    }
    .sub-header {
        color: #8b949e;
        font-size: 1rem;
        margin-bottom: 2.5rem;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }

    /* Card Styling - Uniform Size */
    .news-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        height: 340px; /* Fixed height for uniformity */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .news-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        border-color: #0072ff;
    }

    /* Title Truncation */
    .news-title {
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 12px;
        line-height: 1.3;
        
        display: -webkit-box;
        -webkit-line-clamp: 2; /* Limit to 2 lines */
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Summary Truncation */
    .news-summary {
        color: #8b949e;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: auto; /* Push meta to bottom */
        
        display: -webkit-box;
        -webkit-line-clamp: 3; /* Limit to 3 lines */
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .news-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #30363d;
    }

    .news-date {
        color: #58a6ff;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .read-more-btn {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        background: rgba(0, 114, 255, 0.1);
        border: 1px solid rgba(0, 114, 255, 0.3);
        color: #58a6ff !important;
        text-decoration: none !important;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .read-more-btn:hover {
        background: #0072ff;
        color: #ffffff !important;
        border-color: #0072ff;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
st.sidebar.markdown("## 🔍 SETTINGS")
search_query = st.sidebar.text_input("Search Topic", value="生成AI")

st.sidebar.markdown("### QUICK FILTERS")
filters = {
    "Generative AI": "Generative AI",
    "LLM": "Large Language Models",
    "Robotics": "Robotics AI",
    "Business": "AI Business",
    "Startups": "AI Startups"
}

selected_filter = st.sidebar.radio("Select Preset:", ["Custom"] + list(filters.keys()))

if selected_filter != "Custom":
    search_query = filters[selected_filter]

# --- Function to Fetch News ---
@st.cache_data(ttl=300, show_spinner=False)
def fetch_news(query):
    # Encode query for URL
    encoded_query = query.replace(" ", "%20")
    # Japanese RSS Endpoint
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(rss_url)
    return feed.entries

# --- Helper to clean HTML (Basic) ---
import re
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

# --- Main Layout ---
st.markdown('<div class="main-header">AI VANGUARD</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">LATEST INTELLIGENCE ON: <b>{search_query}</b></div>', unsafe_allow_html=True)

if search_query:
    with st.spinner(f"SEARCHING FOR '{search_query}'..."):
        news_items = fetch_news(search_query)

    if news_items:
        # Limit to 20 items
        news_items = news_items[:20]
        
        # Responsive Grid Layout
        cols = st.columns(3)
        
        for i, entry in enumerate(news_items):
            # Clean up date
            try:
                dt = parser.parse(entry.published)
                # Format: 2023.10.27
                published_str = dt.strftime("%Y.%m.%d")
            except:
                published_str = entry.published[:10]
            
            # Clean Summary
            raw_summary = entry.summary if 'summary' in entry else ""
            clean_summary = clean_html(raw_summary)
            # Use CSS for truncation, but keep raw text reasonable size
            if len(clean_summary) > 200:
                clean_summary = clean_summary[:200] + "..."

            # distribute cards across columns
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="news-card">
                        <div>
                            <div class="news-title">{entry.title}</div>
                            <div class="news-summary">{clean_summary}</div>
                        </div>
                        <div class="news-meta">
                            <span class="news-date">{published_str}</span>
                            <a href="{entry.link}" target="_blank" class="read-more-btn">READ MORE</a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No signals found. Try adjusting frequencies.")
else:
    st.info("👈 Initialize search sequence.")
