
import streamlit as st
import requests
import json
import pandas as pd
import openai
import os

from streamlit_extras.stateful_button import button
from streamlit_extras.badges import badge
from streamlit_extras.stylable_container import stylable_container

# Load secrets from environment variables for deployment
SEFARIA_API_KEY = os.getenv("SEFARIA_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

SEFARIA_BASE_URL = "https://www.sefaria.org/api"

def sefaria_get(endpoint, params=None, api_key=None):
    url = f"{SEFARIA_BASE_URL}/{endpoint}"
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as http_err:
        return None, f"HTTP error occurred: {http_err}"
    except Exception as err:
        return None, f"Other error occurred: {err}"

def ask_llm(memory, openai_key):
    openai.api_key = openai_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=memory
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)

st.set_page_config(page_title="Sefaria LLM Explorer", layout="wide", page_icon="📖", initial_sidebar_state="expanded")

with stylable_container("header", css="""
    #header {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    h1 {
        color: #2d6cdf;
    }
"""):
    st.title("📖 Sefaria + LLM Streamlit App (Deployment Ready)")
    badge(type="github", name="View on GitHub", url="https://github.com/Sefaria/Sefaria-Project")

if "memory" not in st.session_state:
    st.session_state.memory = [
        {"role": "system", "content": "You are a helpful expert on Jewish texts. You use Sefaria data to answer questions."}
    ]

if "full_history" not in st.session_state:
    st.session_state.full_history = []

with stylable_container("sidebar", css="""
    [data-testid=stSidebar] {
        background-color: #f0f4fb;
    }
"""):
    st.sidebar.header("🔧 API Keys & Config")
    sefaria_api_key = st.sidebar.text_input("Sefaria API Key (optional)", value=SEFARIA_API_KEY, type="password")
    openai_api_key = st.sidebar.text_input("OpenAI API Key (required)", value=OPENAI_API_KEY, type="password")

st.subheader("Ask a question based on Sefaria data")
user_question = st.text_area("Your Question:", placeholder="e.g. What does Genesis 1:1 say?", height=100)
refs_to_query = st.text_input("References to retrieve (comma separated, e.g. Genesis.1.1, Exodus.2.1):", placeholder="Genesis.1.1, Exodus.2.1")

if st.button("Ask LLM"):
    if not openai_api_key:
        st.error("Please provide your OpenAI API key.")
    elif not refs_to_query or not user_question:
        st.warning("Please provide both references and a question.")
    else:
        with st.spinner("Fetching data from Sefaria API..."):
            all_texts = {}
            refs = [ref.strip() for ref in refs_to_query.split(",") if ref.strip()]
            for ref in refs:
                data, error = sefaria_get(f"texts/{ref}", api_key=sefaria_api_key)
                if error:
                    st.error(f"Error retrieving {ref}: {error}")
                else:
                    all_texts[ref] = data
        if all_texts:
            st.success("✅ Successfully retrieved all requested data from Sefaria!")
            st.subheader("📦 Retrieved Sefaria Data")
            st.json(all_texts)

            combined_context = json.dumps(all_texts)
            prompt = f"The user asked: '{user_question}'. Here is the retrieved text data: {combined_context}. Please answer concisely."
            st.session_state.memory.append({"role": "user", "content": prompt})

            with st.spinner("Asking LLM..."):
                answer, llm_error = ask_llm(st.session_state.memory, openai_api_key)

            if llm_error:
                st.error(llm_error)
            else:
                st.session_state.memory.append({"role": "assistant", "content": answer})
                st.subheader("🤖 LLM Answer")
                st.write(answer)
                st.session_state.full_history.append({
                    "references": refs,
                    "question": user_question,
                    "answer": answer,
                    "sefaria_result": all_texts
                })

with st.expander("📤 Export Session History"):
    if st.button("Export as JSON"):
        st.download_button("Download JSON", data=json.dumps(st.session_state.full_history, indent=2), file_name="sefaria_llm_session.json", mime="application/json")

with stylable_container("history", css="""
    #history {
        background-color: #fefefe;
        border: 1px solid #eee;
        padding: 1rem;
        border-radius: 12px;
    }
"""):
    if st.sidebar.checkbox("📜 Show Full Conversation History") and st.session_state.full_history:
        st.sidebar.write("## Full Session Queries")
        for i, record in enumerate(reversed(st.session_state.full_history)):
            with st.sidebar.expander(f"Query {len(st.session_state.full_history) - i}"):
                st.write("References:", record["references"])
                st.write("Question:", record["question"])
                st.write("LLM Answer:", record["answer"])
                st.write("Sefaria Text Count:", len(record["sefaria_result"]))
