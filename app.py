import pandas as pd
from nrclex import NRCLex
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import requests
import numpy as np

# --- Configuration ---
# Your provided NewsAPI.org key
NEWS_API_KEY = "5d9fa8bb0dfd43dc9bc92b57d3e2a4be" 
NEWS_API_URL = "https://newsapi.org/v2/everything"
EMOTIONS = ['joy', 'anger', 'fear', 'sadness', 'disgust', 'anticipation', 'surprise', 'trust']
# ---------------------

def analyze_emotion(text):
    """Analyzes text for NRC emotions and returns a normalized dictionary of scores."""
    # The NRCLex library is used here, which is a lexicon-based tool for emotion detection.
    emotion_object = NRCLex(text)
    
    # Get raw emotion scores (word counts associated with each emotion)
    raw_scores = emotion_object.raw_emotion_scores
    
    # Calculate simple 'Sentiment' from Positive/Negative words in NRC Lexicon
    # We use this as a quick valence check alongside the detailed emotions.
    sentiment_score = raw_scores.get('positive', 0) - raw_scores.get('negative', 0)
    
    # Calculate the total count of words with *any* emotion/sentiment association
    total_words = sum(raw_scores.get(e, 0) for e in EMOTIONS)
    
    # Normalize scores: calculate frequency of each emotion 
    emotion_freq = {e: raw_scores.get(e, 0) for e in EMOTIONS}
    
    if total_words > 0:
        normalized_freq = {e: count / total_words for e, count in emotion_freq.items()}
    else:
        normalized_freq = {e: 0 for e in EMOTIONS}

    return normalized_freq, sentiment_score

@st.cache_data(ttl=600) # Cache data for 10 minutes to avoid hitting API limits
def load_and_process_live_data(topic):
    """Fetches live news headlines based on a topic and processes emotions."""
    if not topic:
        return None, None

    # 1. API Data Fetch
    params = {
        'q': topic,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 50,  # Request up to 50 articles
        'apiKey': NEWS_API_KEY
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status() # Raise exception for bad status codes
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from News API. Check your API key or network connection: {e}")
        return None, None
    except ValueError:
        st.error("Error: Could not decode JSON response from API.")
        return None, None

    articles = data.get('articles', [])
    if not articles:
        st.warning(f"No recent articles found for topic: '{topic}'. Try a different keyword.")
        return None, None

    st.success(f"Successfully fetched {len(articles)} articles for '{topic}'.")

    # 2. Emotional Analysis and Feature Extraction
    results = []
    for article in articles:
        # Use article title for emotional analysis
        text_to_analyze = article.get('title', '')
        
        if text_to_analyze:
            emotion_freq, sentiment = analyze_emotion(text_to_analyze)
            
            # Use 'publishedAt' for date, truncate to date only
            article_date = pd.to_datetime(article.get('publishedAt')).tz_localize(None).normalize()
            
            all_features = {'Date': article_date, 'Headline': text_to_analyze, 'Sentiment': sentiment}
            all_features.update(emotion_freq)
            results.append(all_features)

    if not results:
        st.warning(f"No extractable headlines found in fetched articles for '{topic}'.")
        return None, None
        
    df_results = pd.DataFrame(results)
    
    # 3. Aggregate Daily Data (The "Mood" Calculation)
    df_daily = df_results.groupby('Date').agg(
        **{
            'Sentiment': ('Sentiment', 'mean'),
            **{e: (e, 'mean') for e in EMOTIONS}
        }
    ).reset_index()

    return df_daily, df_results

def display_sentiment_arc(df_daily, topic):
    """Generates the Sentiment Time Series Plot."""
    st.subheader(f" Daily Average News Sentiment for '{topic}' (Mood Arc)")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df_daily, x='Date', y='Sentiment', marker='o', color='blue', label='Average Sentiment', ax=ax)
    ax.axhline(0, color='red', linestyle='--', linewidth=0.8, label='Neutral')
    ax.set_title(f'Sentiment Trend Over Time', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sentiment Score (Positive/Negative)')
    ax.grid(True, linestyle=':', alpha=0.7)
    st.pyplot(fig)

def display_emotion_affect(df_daily, topic):
    """Generates the Emotion Stacked Area Plot."""
    st.subheader(f" Daily Emotional Tone Distribution for '{topic}' (Affect)")
    
    # Set the Date as the index for plotting
    df_plot = df_daily.set_index('Date')[EMOTIONS]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Use a visually distinct color map for the emotions
    df_plot.plot(kind='area', stacked=True, alpha=0.8, ax=ax, cmap='tab20') 
    ax.set_title(f'Distribution of Affect Over Time', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Emotion Frequency')
    ax.legend(title='Emotion', loc='upper left', bbox_to_anchor=(1.05, 1))
    ax.grid(axis='y', linestyle=':', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)


# --- Streamlit Application Main Function ---
st.set_page_config(page_title="Emotional News Analyzer", layout="wide")
st.title(" NLP for Emotional Intelligence: Live Emotional News Analyzer")
st.markdown("---")

st.sidebar.header("Analyzer Settings")

# 1. User Input in Sidebar
topic = st.sidebar.text_input(
    "Enter News Topic:", 
    value="AI", 
    help="Type a topic (e.g., 'Apple', 'Climate Change', 'Election') and press Enter."
)

# 2. Load and Process Data (Caches results for 10 min)
if topic:
    df_daily, df_results = load_and_process_live_data(topic)
else:
    st.info("Please enter a news topic in the sidebar to start the analysis.")
    df_daily, df_results = None, None

if df_daily is not None:
    st.header(f"Analysis Results for: **{topic}**")
    st.write(
        "This tool visualizes the collective **Mood** (Sentiment) and **Affect** (Specific Emotions) "
        "of the last 50 news headlines regarding your chosen topic, showing trends over time."
    )

    # Display raw data for transparency
    with st.expander(f"View Raw Data and Emotion Scores ({len(df_results)} headlines)"):
        st.dataframe(df_results[['Date', 'Headline', 'Sentiment'] + EMOTIONS], use_container_width=True)

    # Display visualizations
    display_sentiment_arc(df_daily, topic)
    display_emotion_affect(df_daily, topic)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**API Key Used:** `{NEWS_API_KEY[:4]}...{NEWS_API_KEY[-4:]}`")
