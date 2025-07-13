from serpapi import GoogleSearch
from config import CONFIG
from utils.logger import log_action

def search_and_scrape(st):
    st.subheader("🔍 Google Search with SerpAPI")
    query = st.text_input("Enter Search Query:", key="search_query")

    if st.button("Search"):
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": CONFIG['serpapi']['api_key']
            })
            results = search.get_dict().get("organic_results", [])
            st.subheader("Top 5 Google Results")
            for r in results[:5]:
                st.markdown(f"- **[{r.get('title')}]({r.get('link')})**\n\n{r.get('snippet')}")
            log_action(f"Searched: {query}")
        except Exception as e:
            st.error(f"❌ Search error: {str(e)}")
            log_action(f"Search error: {str(e)}")

def search_response_with_serpapi(query):
    search = GoogleSearch({
        "q": query,
        "api_key": CONFIG['serpapi']['key'],
    })
    results = search.get_dict()
    return results.get("organic_results", [])[:3]