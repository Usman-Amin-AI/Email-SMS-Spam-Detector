import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Spam Detector | Email & SMS",
    page_icon="📧",
    layout="centered"
)

# -------------------------------
# Custom CSS (Light + Dark mode)
# -------------------------------
st.markdown("""
    <style>
        :root {
            --bg-color-light: #f7f9fc;
            --text-color-light: #1f2937;
            --card-color-light: #ffffff;
            --border-color-light: #dcdcdc;

            --bg-color-dark: #0f172a;
            --text-color-dark: #f8fafc;
            --card-color-dark: #1e293b;
            --border-color-dark: #334155;
        }

        @media (prefers-color-scheme: dark) {
            body {
                background-color: var(--bg-color-dark);
                color: var(--text-color-dark);
            }
            .stTextArea textarea {
                background-color: var(--card-color-dark);
                color: var(--text-color-dark);
                border: 1px solid var(--border-color-dark);
            }
            .stButton>button {
                background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
                color: #fff;
            }
            .main-title {
                color: #f1f5f9;
            }
            .sub-title {
                color: #94a3b8;
            }
        }

        @media (prefers-color-scheme: light) {
            body {
                background-color: var(--bg-color-light);
                color: var(--text-color-light);
            }
            .stTextArea textarea {
                background-color: var(--card-color-light);
                border: 1px solid var(--border-color-light);
                color: var(--text-color-light);
            }
            .stButton>button {
                background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
                color: #fff;
            }
            .main-title {
                color: #1f2937;
            }
            .sub-title {
                color: #555;
            }
        }

        .stTextArea textarea {
            border-radius: 12px;
            font-size: 16px;
            line-height: 1.5;
        }
        .stButton>button {
            border-radius: 10px;
            padding: 0.6em 1.4em;
            font-size: 17px;
            font-weight: 500;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.03);
        }
        .main-title {
            font-size: 36px;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.2em;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            margin-bottom: 1.5em;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# NLTK Setup
# -------------------------------
nltk.download('punkt')
nltk.download('stopwords')
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# -------------------------------
# Load Model & Vectorizer
# -------------------------------
@st.cache_resource
def load_model():
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    return tfidf, model

tfidf, model = load_model()

# -------------------------------
# Text Preprocessing
# -------------------------------
def transform_text(text):
    text = text.lower().strip()
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if i.isalnum()]
    tokens = [ps.stem(i) for i in tokens if i not in stop_words and i not in string.punctuation]
    return " ".join(tokens)

# -------------------------------
# UI Layout
# -------------------------------
st.markdown("<div class='main-title'>📧 Email & SMS Spam Detector</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Detect spam instantly</div>", unsafe_allow_html=True)

input_sms = st.text_area("Enter your message below:")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_button = st.button("🔍 Analyze Message")

if predict_button:
    if input_sms.strip() == "":
        st.warning("⚠️ Please enter a message to analyze.")
    else:
        transformed_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transformed_sms]).toarray()
        result = model.predict(vector_input)[0]

        if result == 1:
            st.error("🔴 **This message is Spam**")
            st.markdown("This looks like a promotional, scam, or phishing message. Be cautious.")
        else:
            st.success("🟢 **This message is Not Spam**")
            st.markdown("Looks clean and safe! No spam indicators found.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
    <hr>
    <div style='text-align: center; color: gray; font-size: 14px;'>
                      <b>Made By Usman Amin</b><br>
        <span style='opacity: 0.8;'>© 2025 AI Spam Detector Project</span>
    </div>
""", unsafe_allow_html=True)
