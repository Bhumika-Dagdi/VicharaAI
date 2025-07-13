import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import os
from serpapi import GoogleSearch

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def extract_text_from_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df.to_string(index=False)

def serpapi_doc_search(query):
    search = GoogleSearch({
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
    })
    return search.get_dict().get("organic_results", [])

def chat_with_file_serpapi():
    st.subheader("📁 Chat with PDF/CSV using SerpAPI")

    file = st.file_uploader("Upload PDF or CSV file", type=["pdf", "csv"])

    if file:
        ext = file.name.split(".")[-1].lower()
        if ext == "pdf":
            content = extract_text_from_pdf(file)
        elif ext == "csv":
            content = extract_text_from_csv(file)
        else:
            st.error("Unsupported file type.")
            return

        st.success("Text extracted successfully.")
        st.text_area("🔍 Document Preview", content[:1000], height=200)

        question = st.text_input("Ask a question (keyword-based):")
        if st.button("🔎 Search using SerpAPI"):
            if not question.strip():
                st.warning("Please enter a question.")
                return

            query = f"{question} based on: {content[:300]}"
            results = serpapi_doc_search(query)

            if results:
                st.markdown("### 📚 Top Results")
                for r in results[:5]:
                    st.markdown(f"- **[{r.get('title')}]({r.get('link')})**\n{r.get('snippet')}")
            else:
                st.warning("No relevant results found.")
