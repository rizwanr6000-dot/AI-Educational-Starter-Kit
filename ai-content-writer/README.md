# AI Content Writer

A small full-stack web app where you pick a **content type** (Article, Blog,
LinkedIn Post, Email, Report) and get AI-generated output formatted to match
that type.

## Folder structure

```
ai-content-writer/
├── backend/
│   ├── app.py                  # Flask server + /generate API route
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Copy to .env and add your API key
│   └── generators/
│       ├── __init__.py
│       ├── llm_client.py       # Shared Claude API wrapper
│       ├── article.py          # Article prompt + formatting rules
│       ├── blog.py             # Blog prompt + formatting rules
│       ├── linkedin.py         # LinkedIn post prompt + formatting rules
│       ├── email.py            # Email prompt + formatting rules
│       └── report.py           # Report prompt + formatting rules
├── frontend/
│   ├── index.html              # Single-page UI
│   ├── style.css               # Dark-mode styling
│   └── script.js                # Calls the backend /generate endpoint
└── README.md
```

## How it works

1. The user selects a content type + tone and types a topic in the browser.
2. `script.js` sends this as JSON to `POST /generate`.
3. `app.py` routes the request to the matching module in `generators/`
   (e.g. `content_type=blog` → `generators/blog.py`).
4. Each generator module has its own **system prompt** tailored to that
   format (headline + subheadings for articles, hook + hashtags for
   LinkedIn, subject line + sign-off for email, etc.), and calls
   `llm_client.call_llm()` to get the AI response.
5. The formatted text is returned as JSON and rendered in the output panel.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and paste your key:
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

python app.py
```

Then open **http://localhost:5000** in your browser.

> Note: without an API key set, the app still runs and returns a clearly
> labeled "DEMO MODE" placeholder response, so you can test the full flow
> (frontend → backend → routing → response) before adding real credentials.

## Adding a new content type (e.g. "Twitter Thread")

1. Create `backend/generators/twitter.py` with a `generate(topic, tone, extra_instructions)` function and its own system prompt.
2. Import it in `backend/app.py` and add it to the `GENERATORS` dict:
   ```python
   from generators import twitter
   GENERATORS["twitter"] = twitter.generate
   ```
3. Add a matching `<option value="twitter">Twitter Thread</option>` in `frontend/index.html`.

## Deploying

- Any host that runs Python works (Render, Railway, Fly.io, a VPS, etc.).
- Set `ANTHROPIC_API_KEY` as an environment variable on the host — don't commit `.env`.
- For production, run with a WSGI server instead of Flask's dev server, e.g.:
  ```bash
  pip install gunicorn
  gunicorn app:app
  ```
