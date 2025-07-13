import streamlit as st
import datetime
import requests
import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.logger import log_action

API_URL = "https://api.api-ninjas.com/v1/horoscope"

# ------------------- ML Setup -------------------
def train_horoscope_model():
    # Use a relative path instead of hardcoding full path
    data_path = os.path.join("utils", "data", "Daily_Horoscope.csv")

    if not os.path.exists(data_path):
        st.error(f"🚫 Dataset not found at `{data_path}`.")
        st.info("Please ensure the Daily_Horoscope.csv file is present in `utils/data/` folder.")
        st.stop()

    data = pd.read_csv(data_path)

    # If dataset contains Date and Source columns
    if "Date" in data.columns and "Source" in data.columns:
        data.columns = data.columns.str.strip()
        long_df = pd.melt(
            data,
            id_vars=["Date", "Source"],
            var_name="Sign",
            value_name="Horoscope"
        )
        long_df["Sign"] = long_df["Sign"].str.extract(r'([A-Za-z]+)')
        long_df.dropna(inplace=True)
    else:
        # Assume a flat format with zodiac, mood, age, horoscope
        long_df = data

    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(long_df['Horoscope'])
    y = long_df['Sign']

    model = LogisticRegression(max_iter=2000)
    model.fit(X, y)

    return model, vectorizer

# ------------------- ZODIAC Logic -------------------
def get_zodiac_sign(day, month):
    signs = [
        ("Capricorn", (12, 22), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21)),
        ("Capricorn", (12, 22), (12, 31)),
    ]
    for sign, start, end in signs:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "Capricorn"

# ------------------- Horoscope Hybrid -------------------
def predict_horoscope():
    st.subheader("🔮 Hybrid Horoscope: Live + ML Prediction")

    name = st.text_input("Your Name")
    dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    mood = st.selectbox("Your Current Mood", ["Happy", "Anxious", "Energetic", "Tired", "Neutral"])
    api_key = st.text_input("API Ninjas Key", type="password")

    if st.button("🔍 Predict Horoscope"):
        if not name or not api_key:
            st.warning("Please fill all fields and provide your API key.")
            return

        zodiac = get_zodiac_sign(dob.day, dob.month)
        age = datetime.date.today().year - dob.year

        st.write(f"🌟 Hello **{name}**, your zodiac is **{zodiac}** and you’re **{age}** years old.")

        # Call Horoscope API
        try:
            res = requests.get(
                API_URL,
                params={"zodiac": zodiac},
                headers={"X-Api-Key": api_key}
            )
            data = res.json()
            api_text = data.get("horoscope", "Could not fetch API response.")
        except Exception as e:
            st.error(f"API call failed: {e}")
            return

        # ML Model prediction
        model, vectorizer = train_horoscope_model()
        ml_pred = model.predict(vectorizer.transform([api_text]))[0]

        # Final Combined Output
        st.success("✅ Here's your hybrid horoscope prediction:")
        st.info(f"🧠 **ML Insight**: {ml_pred}")
        st.info(f"🌐 **Today’s Horoscope (Live)**: {api_text}")
        log_action(f"Hybrid Horoscope: {name} | {zodiac} | {mood} | API: {api_text[:60]}")
