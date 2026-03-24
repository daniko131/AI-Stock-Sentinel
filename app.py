import streamlit as st
import yfinance as yf
from transformers import pipeline

# עיצוב בסגנון Apple
st.set_page_config(page_title="Stock Sentinel AI", page_icon="🍏", layout="centered")

st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #ffffff; color: #1d1d1f; font-family: -apple-system, sans-serif; }
    .stMetric { background-color: #f5f5f7; padding: 20px; border-radius: 18px; }
    .stButton>button { background-color: #0071e3; color: white; border-radius: 25px; padding: 10px 30px; border: none; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

classifier = load_model()

st.title("Stock Sentinel")
st.caption("Simple. Powerful. AI Intelligence.")

ticker = st.text_input("Enter Symbol (e.g. NVDA)", "NVDA").upper()

if st.button("Analyze"):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        st.metric(label="Market Price", value=f"${price:.2f}")
        
        st.write("---")
        st.subheader("Latest Intelligence")
        
        news = stock.news
        if news:
            for item in news[:3]:
                title = item.get('title') or item.get('headline')
                analysis = classifier(title)[0]
                sentiment = "Positive ✅" if analysis['label'] == 'POSITIVE' else "Caution ⚠️"
                with st.expander(f"{title}"):
                    st.write(f"AI Sentiment: {sentiment}")
                    st.progress(analysis['score'])
        else:
            st.info("No recent news found.")
    except:
        st.error("Asset not found.")
