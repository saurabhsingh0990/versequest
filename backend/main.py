from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv() # loads variables from a .env file in the current working directory

PPLX_API_KEY = os.getenv("PPLX_API_KEY") # Set in shell: export PPLX_API_KEY=your_key
PPLX_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar-pro" # Use 'pplx-70b-online' only if you truly need web browsing

app = FastAPI(title="VerseQuest - Lyrics-to-Meaning API")

# CORS for local Svelte dev server
app.add_middleware(
CORSMiddleware,
allow_origins=[
"http://localhost:5173",
"http://127.0.0.1:5173",
"http://localhost:8000",
"http://127.0.0.1:8000",
"null" # allows file:// origin preflights in some browsers
],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

class ExplainRequest(BaseModel):
    """
    Incoming request body to analyze lyrics or poetic text.
    - text: the lyrics/content to analyze
    - lang: optional language code (default 'en')
    """
    text: str
    lang: str | None = "en"

class ExplainResponse(BaseModel):
    """
    Outgoing response body ensuring a consistent, typed JSON shape.
    """
    tldr: str
    themes: list[str]
    imagery: list[str]
    cultural_notes: list[str]
    tone: str

def call_pplx(messages: list[dict], system: str | None = None, temperature: float = 0.35, max_tokens: int = 700) -> dict:
    """
    Calls Perplexity's Chat Completions API with provided messages and returns the JSON response.
    Raises HTTP 500/502 on configuration or upstream errors.
    """
    if not PPLX_API_KEY:
        raise HTTPException(status_code=500, detail="Missing PPLX_API_KEY environment variable")
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": MODEL,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": ([{"role": "system", "content": system}] if system else []) + messages,
    }

    try:
        resp = requests.post(PPLX_URL, headers=headers, json=body, timeout=30)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"PPLX request failed: {e}")

    if not resp.ok:
        raise HTTPException(status_code=502, detail=f"PPLX error {resp.status_code}: {resp.text}")

    return resp.json()

@app.get("/")
def root():
    """Quick check that service is up."""
    return {"service": "versequest-backend", "status": "running"}

@app.get("/health")
def health():
    """Health endpoint for monitoring."""
    return {"status": "ok"}

@app.post("/api/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    """
    Analyze lyrics/poetic text and return a structured JSON with:
    - tldr: one-sentence summary
    - themes: 3–6 themes
    - imagery: 3–6 metaphors/images (briefly explained)
    - cultural_notes: references if relevant
    - tone: 1–3 descriptive words
    """
    # 1) Validate and trim input
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Missing text")
    text = text[:6000]  # hard cap to avoid excessive tokens/cost

    # 2) Build system and user prompts
    system = (
    "You are a precise music-meaning analyst.\n"
    "Output MUST be ONLY a single valid JSON object with keys exactly:\n"
    '{ "tldr": string, "themes": string[], "imagery": string[], "cultural_notes": string[], "tone": string }.\n'
    "Do not include Markdown, code fences, or any text before/after the JSON. No comments. No explanations."
    )

    user = f"""
    Analyze the following lyrics (language={req.lang}) and return ONLY JSON with these keys:

    tldr: one-sentence plain summary of meaning (string)

    themes: 3-6 concise themes (array of strings)

    imagery: 3-6 notable images/metaphors with brief explanations (array of strings)

    cultural_notes: 1-5 cultural/linguistic references if relevant, else [] (array of strings)

    tone: 1-3 words (string), e.g., melancholic, rebellious, hopeful

    Lyrics:
    {text}
    """
    # 3) Call Perplexity API
    data = call_pplx(
        messages=[{"role": "user", "content": user}],
        system=system,
        temperature=0.35,
        max_tokens=650,
    )

    # 4) Extract assistant reply content
    content = ""
    try:
        choices = data.get("choices", [])
        if isinstance(choices, list) and choices:
            message = choices[0].get("message", {})
            content = message.get("content", "")
        else:
            content = ""
    except Exception as e:
        print("Extraction error:", e)
        content = ""

    print(content)
    print("RAW CONTENT (first 200 chars):", content[:200])

    # 5) Parse JSON (fall back to safe minimal object if parsing fails)
    try:
        parsed = json.loads(content)
    except Exception:
        parsed = {
            "tldr": content[:800] if content else "No summary available.",
            "themes": [],
            "imagery": [],
            "cultural_notes": [],
            "tone": "neutral",
        }

    # 6) Normalize and enforce types/limits for stability
    for key in ["tldr", "themes", "imagery", "cultural_notes", "tone"]:
        if key not in parsed:
            parsed.setdefault(key, [] if key in ("themes", "imagery", "cultural_notes") else "neutral")

    parsed["tldr"] = str(parsed.get("tldr", "")).strip()
    parsed["tone"] = str(parsed.get("tone", "neutral")).strip()

    parsed["themes"] = [str(x).strip() for x in (parsed.get("themes") or [])][:6]
    parsed["imagery"] = [str(x).strip() for x in (parsed.get("imagery") or [])][:6]
    parsed["cultural_notes"] = [str(x).strip() for x in (parsed.get("cultural_notes") or [])][:5]

    # 7) Return as typed response
    return ExplainResponse(**parsed)

