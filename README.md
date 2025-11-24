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

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sudara17/Emotional_News_Analyzer.git
cd Emotional_News_Analyzer
2️⃣ Create & Activate the Virtual Environment (Windows)
bash
Copy code
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
🔑 Configure Your NewsAPI Key
This project requires a NewsAPI key.

Create one here:
👉 https://newsapi.org/

Then set your key as an environment variable:

bash
Copy code
setx NEWS_API_KEY "your_api_key_here"
⚠️ After running this command, close and reopen your terminal.

▶️ Running the Application
bash
Copy code
streamlit run app.py
OR

bash
Copy code
python -m streamlit run app.py
Once started, open the URL shown (usually):

arduino
Copy code
http://localhost:8501
📁 Project Structure
Copy code
📂 Emotional_News_Analyzer
├── app.py
├── requirements.txt
└── README.md
⚠️ Notes
❌ Do not commit API keys.

✔ Environment variables are already used for safety.

✔ Works best with English-based news topics.

🌱 Future Enhancements
Deployment on Streamlit Cloud

Multi-language sentiment analysis

Exportable emotional analysis reports

👩‍💻 Author
Sudara T S M

If you found this project helpful, ⭐ star the repository!
