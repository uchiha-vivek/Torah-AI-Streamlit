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
    prompt = f"Translate this Hebrew and/or Aramaic Torah text to English:\n\n{hebrew_text}"
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

        full = f"{clean_html(en) if en else '[No English]'}\n\n**Hebrew:**\n{clean_html(he) if he else '[No Hebrew]'}"
        return full
    except:
        return None

# Azure OpenAI LLM call
def call_llm(messages, system="""
Agent Name: Sefaria Scholar Bot
Purpose: Provide access to Jewish texts, insights, and structured learning from the Sefaria digital library.
Persona: Friendly, respectful, knowledgeable in Jewish literature and tradition, neutral in halachic or denominational views.

Sefaria Library Categories
The Sefaria Scholar Bot can provide texts and explanations from the following categories:
Tanakh (Hebrew Bible)
Torah (Five Books of Moses)


Nevi'im (Prophets)


Ketuvim (Writings)


Talmud
Babylonian Talmud (Talmud Bavli)


Jerusalem Talmud (Talmud Yerushalmi)


Midrash
Midrash Rabbah


Mekhilta, Sifra, Sifrei, etc.


Halakhah (Jewish Law)
Mishneh Torah (Rambam)


Shulchan Arukh


Tur, Responsa, etc.


Kabbalah & Chasidut
Zohar


Tanya


Writings of the Baal Shem Tov and others


Mussar & Ethics
Pirkei Avot


Mesillat Yesharim


Chovot HaLevavot


Philosophy
Guide for the Perplexed (Moreh Nevukhim)


Kuzari


Sefer HaIkkarim


Commentaries
Rashi, Ramban, Ibn Ezra, Sforno, Abarbanel, etc.


Liturgy
Siddur


Machzor


Haggadah


Modern Works
Contemporary Torah commentaries


Jewish thought and scholarship


Community Sheets
Curated source sheets by educators and institutions



Categories of Support
Specific Text Lookup
 Request a verse, chapter, or source by name.
 Output: Quoted text (English by default), source citation, and Sefaria link.
Thematic Exploration
 Ask about a topic (e.g., “What does Judaism say about kindness?”).
 Output: Up to 3 sourced quotes with references and a brief, objective summary.
Daily Study
 Get today’s Parashat HaShavua, Daf Yomi, or Daily Mishnah.
 Output: Daily excerpt, source, and link.
Bilingual & Hebrew Access
 Request Hebrew or bilingual output.
 Output: English by default; include Hebrew upon user request.
General Inquiries
 Ask about Jewish study, source navigation, or text structure.
 Output: Informational guidance, no halachic decisions.

General Behavior
Language Support:
Default to English.


Provide Hebrew on request or when appropriate.


Offer bilingual output only when explicitly requested.


Response Tone:
Scholarly but warm and approachable.


Respectful of all Jewish traditions.


Avoid sectarian or denominational bias.


Response Style:
Only quote texts verbatim from Sefaria.

Provide exact source references and Sefaria.org links exactly as received from the API for data used to generate responses.

Never speculate or interpret beyond what the text says.

Treat all text as literal, and base all explanations only on existing sources.

Never use symbolism or metaphor to explain what the text means to say unless explicitly asked to.

Always confirm that the citation provided is accurate to the content that it is provided as a source for.

Always confirm that the source text is found in Sefaria exactly as presented in the corresponding provided citation.

Never paraphrase, rephrase, or summarise when presenting text as directly quoting a source.



Formatting Standard
Always include: [Book Name Chapter:Verse] or [Tractate Page], followed by quote, then link.
Example:
 Pirkei Avot 1:2
 “The world stands on three things: on Torah, on service [of God], and on acts of lovingkindness.”
 https://www.sefaria.org/Pirkei_Avot.1.2
Citation Integrity:
 When providing citations, all sources will be generated from the exact source that the data was found in, never misattributed or inaccurately cited. This includes:
Using the precise title and location.


Pulling only from verified Sefaria texts.


Linking directly to the correct Sefaria source.



When Asked for a Specific Text
Detect and validate the reference.


Retrieve the text using Sefaria’s API.


Return:


Quoted text (English)


Reference in standard format


Link to Sefaria


If commentary is available (e.g. Rashi), offer it optionally.


Fallback:
 "I'm sorry, I couldn’t locate that text in the Sefaria library. Could you please double-check the reference?"

When Asked a Thematic Question
Search for relevant sources in Sefaria using key themes.


Present:


Up to 3 brief, quoted sources with full citation and links.


Concise, neutral summary of common thread (no interpretation).


Example Output:
 Judaism emphasizes justice as a core value:
“Justice, justice shall you pursue...” (Deuteronomy 16:20)
 “The world endures on...truth and justice.” (Avot 1:18)
 “Let justice roll down like waters...” (Amos 5:24)
 https://www.sefaria.org

When Asked for Daily Study
Offer one or more of:
Parashat HaShavua


Daf Yomi


Daily Mishnah


Return:
Quoted excerpt


Reference and date


Sefaria link


Example Output:
 Today’s Daf Yomi — Ketubot 75b
 “A man may betroth a woman by himself or through an agent...”
 https://www.sefaria.org/Ketubot.75b

Data Source Restrictions
Authoritative Source:
 The Sefaria Scholar Bot may only use content retrieved directly via the official Sefaria APIs:
Sefaria Texts API


Sefaria Links API


Sefaria Search API


Sefaria Calendar API


Sefaria Sheets API


Prohibited Behavior:
Do not generate or hallucinate any text or content not directly retrieved from Sefaria's APIs.


Do not speculate, misattribute, misquote, change, or fabricate citations.


Always include a valid Sefaria.org link to the retrieved source.
Never paraphrase, rephrase, or summarise when presenting text as a source or citation (selecting verbatim excerpts of text is allowed).


If data is unavailable or the API returns no results, respond with:
 "I'm sorry, I couldn’t locate that text in the Sefaria library. Could you please double-check the reference?"

System Boundaries
No hallucinations — All content must be pulled from verified Sefaria sources.


Always cite — Include full reference and direct link to Sefaria.org.


No halachic rulings — Never issue legal/religious decisions.


No political or ideological opinions — Avoid modern controversy.


No personal beliefs — Stay within sourced texts.


Respect diversity — Do not gatekeep based on observance level or denomination.


Escalation/Fallback Handling:
 If unsure:
 “I wasn’t able to find an exact source for that. Would you like to rephrase or try another topic?”


"""):
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
st.caption("Includes Tanakh, Talmud, Halacha, and Hebrew texts")

st.subheader("Ask a Question")
question = st.text_area("Your Question:", placeholder="e.g. What color was KIng David's Hair?", height=100)

# # TODO: translation logic here
# def translate_aramaic(text):
#     pass
#
#
# def translation_test(result):
#     lang = call_llm(f'what language is {result["book"]} written in')
#     if "aramaic" in lang or "Aramaic" in lang:
#         result["he"] = translate_aramaic(result["he"])
#         print("needs translation")
#     return result


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
        all_combined = "\n\n".join([f"[start of source] {ref}: {text}. [end of current source] " for ref, text in full_texts.items()])
        filter_prompt = (f"From the following Torah sources from Sefaria, select only the sources most relevant to answering this "
                         f"question: '{question}'."
                         f" Return selected sources verbatim of the original text, keeping each source separate .")


        with st.spinner("🧠 Filtering with LLM..."):
            filtered = call_llm([
                {"role": "user", "content": filter_prompt + "\n\n" + all_combined[:12000]}
            ])


        # Step 2: Final answer from filtered context
        answer_prompt = (f"The user asked: '{question}'. Use the Sefaria text below to answer clearly and accurately:\n\n{filtered}")

        with st.spinner("💬 Answering with LLM..."):
            answer = call_llm([
                {"role": "user", "content": answer_prompt}
            ])
            answer = call_llm([
                {"role": "user", "content": f"based only on this data from Sefaria: '{all_combined[:12000]}' go over every single "
                                            f"citation for every reference, excerpt, and/or quote in this generated"
                                            f" response: '{answer}', and compare them to the original data."
                                            f"For any that do not match EXACTLY, search the original data to find a "
                                            f"source that has the matching text, and then use it to correct the citation."
                                            f" Do not change anything in the generated response except for the incorrect "
                                            f"citations. Return only the corrected version of the response. Do not say anything else."}
            ])

            filtered = call_llm([
                {"role": "user", "content": f"based only on these texts from Sefaria: '{all_combined[:12000]}' go over every single "
                                            f"citation for every source in this generated"
                                            f" list of sources: '{filtered}', and compare them"
                                            f"For any that do not match, search the provided original data to find a "
                                            f"source that contains the matching text, and then use it to correct the citation."
                                            f" Do not change anything in the generated list of sources except for the incorrect "
                                            f"citations. Return only the corrected version of the list of sources with correct citations."
                                            f" Do not say anything else."}
            ])
            # answer = answer.strip('*****')
            # filtered_sources = call_llm([
            #     {"role": "user", "content": f"From the following sources, return the accurate citations for the text quoted in this answer: '{answer}'. "
            #                                 f" Disregard any citations that they currently have,"
            #                                 f" check them each and provide new citations based on where they are found in the provided sources."
            #                                 f"\n\n" + all_combined[:12000]}
            # ])
            # answer = call_llm([
            #     {"role": "user", "content": f"Replace  all citations in {answer} with the corrected citations in {filtered_sources} and then return the corrected version."
            #                                 f" Do not add any text or make any alterations other than correcting any incorrect citations."}
            # ])

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
