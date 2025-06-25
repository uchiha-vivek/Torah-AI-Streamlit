import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
SEFARIA_API_KEY = os.getenv("SEFARIA_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("ENDPOINT_URL")
AZURE_OPENAI_DEPLOYMENT = os.getenv("DEPLOYMENT_NAME")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Init Azure OpenAI client
azure_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2025-01-01-preview",
)

# HTML stripper
def clean_html(raw_html):
    if not raw_html:
        return ""
    return BeautifulSoup(raw_html, "html.parser").get_text(separator=" ", strip=True)

# Search Sefaria across entire corpus
def search_sefaria(query, size=10):
    try:
        resp = requests.get(
            "https://www.sefaria.org/api/v2/search",
            params={"q": query, "size": size, "type": "text", "filters": []}
        )
        if resp.ok:
            data = resp.json()
            return [
                {
                    "ref": hit.get("ref"),
                    "text": clean_html(hit.get("highlight", {}).get("text", [""])[0]),
                    "he": clean_html(hit.get("highlight", {}).get("he", [""])[0]),
                    "score": hit.get("_score", 0)
                }
                for hit in data.get("hits", []) if hit.get("ref")
            ]
        else:
            return []
    except Exception as e:
        return [{"ref": "[error]", "text": str(e), "he": "", "score": 0}]

# Get full text of a ref
def sefaria_get(ref, api_key=None):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(f"https://www.sefaria.org/api/texts/{ref}", headers=headers)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)

# LLM call
def call_llm(messages):
    try:
        response = azure_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        )
        return clean_html(response.choices[0].message.content.strip()), None
    except Exception as e:
        return None, str(e)

# UI setup
st.set_page_config(page_title="Torah AI Deep Search", layout="wide", page_icon="📖")
st.title("📖 Torah AI – Deep Sefaria Search")

# Sidebar options
st.sidebar.header("🔧 Settings")
sefaria_api_key = st.sidebar.text_input("Sefaria API Key (optional)", value=SEFARIA_API_KEY, type="password")

lang_mode = st.sidebar.radio("Display Language", ["English", "Hebrew", "Both"], index=0)
result_count = st.sidebar.slider("Number of References", 3, 20, 10)

# Init session
if "memory" not in st.session_state:
    st.session_state.memory = [{
        "role": "system",
        "content": "You are a Torah AI scholar assistant. Only use text provided. Never speculate."
    }]
if "full_history" not in st.session_state:
    st.session_state.full_history = []

# Main input
st.subheader("Ask a Question")
question = st.text_area("Your Question:", placeholder="e.g. What color was King David’s hair?", height=100)

if st.button("Submit"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("🔍 Searching Sefaria's full library..."):
            search_results = search_sefaria(question, size=result_count)

        fetched_texts = {}
        with st.spinner("📚 Fetching full texts..."):
            for result in search_results:
                ref = result["ref"]
                data, error = sefaria_get(ref, sefaria_api_key)
                if error:
                    fetched_texts[ref] = f"[Error fetching: {error}]"
                else:
                    en = " ".join(data.get("text", [])) or "[No English]"
                    he = " ".join(data.get("he", [])) or "[No Hebrew]"
                    if lang_mode == "English":
                        content = clean_html(en)
                    elif lang_mode == "Hebrew":
                        content = clean_html(he)
                    else:
                        content = f"{clean_html(en)}\n\n**Hebrew:**\n{clean_html(he)}"
                    fetched_texts[ref] = content

        # Compose LLM input
        combined = "\n".join([f"{ref}: {text}" for ref, text in fetched_texts.items()])
        user_prompt = f"The user asked: '{question}'. Use the following Sefaria texts to answer:\n\n{combined}"
        st.session_state.memory.append({"role": "user", "content": user_prompt})

        with st.spinner("💬 Generating answer..."):
            answer, err = call_llm(st.session_state.memory)

        if err:
            st.error(err)
        else:
            st.session_state.memory.append({"role": "assistant", "content": answer})
            st.session_state.full_history.append({
                "question": question,
                "answer": answer,
                "references": fetched_texts
            })

            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("🤖 Answer")
                st.write(answer)

                st.subheader("📘 Source Texts")
                for ref, text in fetched_texts.items():
                    st.markdown(f"**{ref}**")
                    st.write(text)

            with col2:
                st.subheader("🗂️ Session History")
                for item in reversed(st.session_state.full_history):
                    st.markdown(f"- {item['question']}")
                st.download_button("Export JSON", json.dumps(st.session_state.full_history, indent=2),
                                   file_name="session_history.json", mime="application/json")
