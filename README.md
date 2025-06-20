# Sefaria + LLM Streamlit App 🚀

A Streamlit-powered AI assistant that answers questions based on Sefaria Jewish text data using GPT-4o.

## Features
- Retrieve multiple references from Sefaria API
- Use OpenAI GPT-4o for answers
- Maintain conversation history and context
- Export full session as JSON
- Deployable to Streamlit Cloud, Docker, or serverless

## Environment Variables
- SEFARIA_API_KEY (optional)
- OPENAI_API_KEY (required)

## Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect repo on Streamlit Cloud
3. Set secrets under App Settings

### Docker
```bash
docker build -t sefaria-llm .
docker run -p 8501:8501 -e SEFARIA_API_KEY=xxx -e OPENAI_API_KEY=xxx sefaria-llm
```

### How I ran it
1. Run Docker
2. Add an env file with credentials
3. run this command: docker build -t sefaria-llm .
4. after completion, run this command: docker run --env-file .env -p 8501:8501 sefaria-llm
5. open on http://localhost:8501/

### Serverless (Render, Fly.io, Railway)
Use Dockerfile + env vars.
