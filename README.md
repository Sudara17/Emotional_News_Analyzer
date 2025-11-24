# 📰 Emotional News Analyzer

A live NLP-powered Streamlit application that analyzes recent news headlines for **sentiment** and **emotional tone** using the **NRCLex** emotion lexicon.  
It visualizes how news sentiment and emotions fluctuate over time for a given topic.

---

## 🚀 Features

- 🔍 Fetches real-time news using **NewsAPI**
- 🧠 Emotion classification using NRC Emotion Lexicon (NRCLex)
- 📈 Visual reporting:
  - Sentiment trend chart
  - Stacked multi-emotion visualization
- ⚡ Caching enabled to reduce unnecessary API calls
- 🎛 Interactive topic search (ex: "AI", "Sports", "Elections", "Weather")

---

## 📂 Installation & Setup
```bash

1️⃣ Clone the Repository

git clone https://github.com/Sudara17/Emotional_News_Analyzer.git
cd Emotional_News_Analyzer

2️⃣ Create & Activate the Virtual Environment (Windows)

python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Your NewsAPI Key 🔑
This project requires a NewsAPI key.

Create one here:
👉 https://newsapi.org/

setx NEWS_API_KEY "your_api_key_here"

5️⃣ Running the Application

streamlit run app.py
OR
python -m streamlit run app.py

Once started, open the URL shown (usually):
👉 http://localhost:8501


📁 Project Structure

📂 Emotional_News_Analyzer
├── app.py
├── requirements.txt
└── README.md


🌱 Future Enhancements
Deployment on Streamlit Cloud
Multi-language sentiment analysis
Exportable emotional analysis reports

👩‍💻 Author
Sudara T S M
If you found this project helpful, ⭐ star the repository!
