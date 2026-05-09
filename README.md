# content-generation-pipeline

# Content Generation Pipeline

A multi-step AI pipeline that generates a complete content package 
from a single topic. One input produces a blog post, three social 
media captions, and a full email — all in consistent brand tone.

**Live Demo:** [content-generation-pipeline.streamlit.app](https://content-generation-pipeline-kesqucmdq6eyd6wnnbqf7c.streamlit.app)  
**API Docs:** [content-generation-pipeline.onrender.com/docs](https://content-generation-pipeline.onrender.com/docs)

---

## The Pipeline

```
Topic + Tone + Audience
        │
        ▼
Step 1: Generate structured blog outline          [Groq call 1]
        │
        ▼ (outline passed as context)
Step 2: Expand outline into full blog post         [Groq call 2]
        │
        ▼ (blog post passed as context)
Step 3: Summarise the blog post                    [Groq call 3]
        │
        ├─────────────────────┐
        ▼                     ▼
Step 4: Social captions   Step 5: Email copy  [Groq calls 4 & 5]
(LinkedIn, Twitter, Instagram)   (subject, body, CTA)
```

Each step feeds its output into the next.
The summary bridges the blog post to the downstream content pieces,
keeping captions and email focused without passing the full 900-word article.

---

## Key Engineering Decision — Prompt Chaining vs One Big Prompt

A single prompt asking for a blog post, three captions, and an email
produces mediocre output — the LLM splits attention across too many
tasks simultaneously.

Separate focused prompts produce better quality because:
- Each call has one job with clear requirements
- Context from previous steps improves relevance
- Failures are isolated — if step 4 fails, steps 1-3 are not lost
- Individual steps can be improved or replaced without touching the rest

---

## Content Output

| Piece | Format | Length |
|---|---|---|
| Blog Post Outline | Markdown headings | 5 sections |
| Blog Post | Full article | 600–900 words |
| LinkedIn Caption | Text + hashtags | 150–200 chars |
| Twitter Caption | Text + hashtags | Under 240 chars |
| Instagram Caption | Text + hashtags | 100–150 chars |
| Email Subject | Plain text | Under 60 chars |
| Email Body | Marketing copy | 150–200 words |

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| LLM | Groq — Llama 3.3 70B | Content generation |
| Prompt chaining | Custom Python | Sequential calls with context passing |
| Backend | FastAPI | REST API |
| Frontend | Streamlit | Input form and tabbed content display |
| Export | python-docx | Download full package as Word document |
| Containers | Docker + Docker Compose | Environment parity |
| Backend hosting | Render | FastAPI via Docker |
| Frontend hosting | Streamlit Community Cloud | Streamlit deployment |

---

## Project Structure

```
content-generation-pipeline/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── generate.py      # POST /generate, GET /tones
│   │   │   └── health.py        # GET /health
│   │   └── schemas.py           # Request/response Pydantic models
│   ├── core/
│   │   ├── generator.py         # Single Groq call function
│   │   └── prompts.py           # Five prompt templates
│   ├── services/
│   │   └── pipeline.py          # Five-step chain orchestration
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── app.py                   # Streamlit tabbed interface
│   ├── api_client.py            # HTTP client
│   └── config.py
├── tests/
│   ├── test_pipeline.py
│   └── test_api.py
├── Dockerfile
├── Dockerfile.frontend
├── docker-compose.yml
├── .python-version
├── .env.example
└── requirements.txt
```

---

## Running Locally

### Prerequisites
- Python 3.12+
- [Groq](https://console.groq.com) free API key

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/content-generation-pipeline.git
cd content-generation-pipeline

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your GROQ_API_KEY to .env

uvicorn app.main:app --reload --port 8000
```

Frontend (new terminal):
```bash
cd frontend
streamlit run app.py
```

Visit `http://localhost:8501`

### With Docker
```bash
docker compose up --build
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/generate` | Run the full content pipeline |
| `GET` | `/api/v1/generate/tones` | List available tone options |
| `GET` | `/health` | Health check |

Generation takes 15–25 seconds — five sequential LLM calls.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ | — | Groq API key |
| `LLM_MODEL` | ❌ | `llama-3.3-70b-versatile` | Groq model |
| `TEMPERATURE` | ❌ | `0.7` | LLM temperature for creative output |
| `APP_ENV` | ❌ | `development` | Environment name |

---

## Author

**Mubarak Olalekan Oladipo**  
AI Software Engineer  
[GitHub](https://github.com/Mubrix2) · [LinkedIn](https://linkedin.com/in/mubarak-oladipo)