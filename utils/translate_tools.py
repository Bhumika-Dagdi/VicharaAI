import streamlit as st
from deep_translator  import GoogleTranslator

def language_translator():
    st.subheader("🌐 Language Translator")

    text = st.text_area("Enter text to translate")
    src = st.selectbox("Source Language", ["auto", "en", "hi", "fr", "es", "de"])
    dest = st.selectbox("Translate To", ["en", "hi", "fr", "es", "de"])

    if st.button("Translate"):
        try:
            result = GoogleTranslator(source=src, target=dest).translate(text)
            st.text_area("📝 Translated Text", result, height=150)
        except Exception as e:
            st.error(f"❌ Translation failed: {str(e)}")
