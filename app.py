import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("ENDPOINT_URL")
AZURE_OPENAI_DEPLOYMENT = os.getenv("DEPLOYMENT_NAME")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Init OpenAI client
azure_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2025-01-01-preview",
)

# Clean HTML
def clean_html(raw_html):
    if not raw_html:
        return ""
    return BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

# Translate Hebrew using LLM if no English is available
def translate_hebrew(hebrew_text):
    prompt = f"Translate this Hebrew Torah text to English:\n\n{hebrew_text}"
    return call_llm([{"role": "user", "content": prompt}], system="You are a Torah translation assistant.")

# Get full Sefaria text with fallback translation
def get_sefaria_text(ref):
    try:
        resp = requests.get(f"https://www.sefaria.org/api/texts/{ref}")
        if not resp.ok:
            return None
        data = resp.json()
        en = " ".join(data.get("text", []))
        he = " ".join(data.get("he", []))

        if not en.strip() and he.strip():
            en = translate_hebrew(he)

        full = f"{clean_html(en)}\n\n**Hebrew:**\n{clean_html(he) if he else '[No Hebrew]'}"
        return full
    except:
        return None

# Azure OpenAI LLM call
def call_llm(messages, system="You are a Torah scholar AI. Use only the Sefaria text. Never speculate."):
    try:
        response = azure_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system},
                *messages
            ],
            max_tokens=1200,
            temperature=0.7,
            top_p=0.95
        )
        return clean_html(response.choices[0].message.content.strip())
    except Exception as e:
        return f"LLM Error: {e}"

# Deep Sefaria search with enforcement
def search_sefaria(query, max_results=50, filters=[]):
    results = []
    page = 0
    seen_refs = set()

    torah_books = {"Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"}
    torah_hits = {book: None for book in torah_books}
    josephus_hits = []

    try:
        while len(results) < max_results:
            resp = requests.get(
                "https://www.sefaria.org/api/v2/search",
                params={
                    "q": query,
                    "size": 20,
                    "from": page * 20,
                    "type": "text",
                    "filters": filters
                }
            )
            if not resp.ok:
                break
            data = resp.json()
            hits = data.get("hits", [])
            if not hits:
                break

            for hit in hits:
                ref = hit.get("ref")
                book = hit.get("index_title", "")
                category = hit.get("category", "")
                if ref and ref not in seen_refs:
                    seen_refs.add(ref)
                    result = {
                        "ref": ref,
                        "book": book,
                        "category": category,
                        "text": clean_html(hit.get("highlight", {}).get("text", [""])[0]),
                        "he": clean_html(hit.get("highlight", {}).get("he", [""])[0])
                    }

                    if book in torah_hits and torah_hits[book] is None:
                        torah_hits[book] = result
                    if book.startswith("Josephus") and not any(j['book'] == book for j in josephus_hits):
                        josephus_hits.append(result)

                    results.append(result)
                    if len(results) >= max_results:
                        break
            page += 1

        combined = list(filter(None, torah_hits.values())) + josephus_hits + [r for r in results if r not in torah_hits.values() and r not in josephus_hits]
        return combined[:max_results]

    except Exception as e:
        return [{"ref": "[error]", "text": str(e), "he": "", "book": "", "category": ""}]

# --- UI Layout --- #
st.set_page_config(page_title="Torah AI – Deep Search", layout="wide")
st.title("📖 Torah AI ")
st.caption("Includes Tanakh, Talmud, Halacha, Josephus, and Hebrew texts")

st.subheader("Ask a Question")
question = st.text_area("Your Question:", placeholder="e.g. What color was KIng David's Hair?", height=100)

if st.button("Search and Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("🔍 Searching Torah AI..."):
            search_results = search_sefaria(question, max_results=50)

        with st.spinner("📚 Fetching full texts..."):
            full_texts = {}
            for result in search_results:
                ref = result["ref"]
                text = get_sefaria_text(ref)
                if text:
                    full_texts[ref] = text

        # Step 1: Filter with LLM
        all_combined = "\n\n".join([f"{ref}: {text}" for ref, text in full_texts.items()])
        filter_prompt = f"From the following Torah AI sources, pick only the parts most relevant to answering this question: '{question}'. Return them directly."

        with st.spinner("🧠 Filtering with LLM..."):
            filtered = call_llm([
                {"role": "user", "content": filter_prompt + "\n\n" + all_combined[:12000]}
            ])

        # Step 2: Final answer from filtered context
        answer_prompt = f"The user asked: '{question}'. Use the filtered Sefaria text below to answer clearly and accurately:\n\n{filtered}"

        with st.spinner("💬 Answering with LLM..."):
            answer = call_llm([
                {"role": "user", "content": answer_prompt}
            ])

        # Display results
        st.subheader("🤖 Answer")
        st.write(answer)

        st.subheader("📘 Filtered Source Excerpts")
        st.write(filtered)

        st.subheader("📚 All Sources Queried")
        for result in search_results:
            ref = result["ref"]
            book = result.get("book", "")
            tag = result.get("category", "Other")
            if book.startswith("Josephus"):
                tag_display = "📘 Josephus"
            elif tag == "Tanakh":
                tag_display = "🟦 Tanakh"
            elif tag == "Talmud":
                tag_display = "🟥 Talmud"
            else:
                tag_display = f"⬜ {tag}"

            text = full_texts.get(ref)
            if text:
                st.markdown(f"**{ref}** – _{tag_display}_")
                st.write(text)
