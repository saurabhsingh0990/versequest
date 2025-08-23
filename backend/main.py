from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

PPLX_API_KEY = os.getenv("PPLX_API_KEY")
PPLX_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar-pro"

app = FastAPI(title="VerseQuest - Lyrics-to-Meaning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://127.0.0.1:8000", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExplainRequest(BaseModel):
    text: str
    lang: str | None = "en"

class ExplainResponse(BaseModel):
    song_credit: list[str]
    original_lyrics: list[str]
    meaning_lyrics: list[str]
    tldr: str
    themes: list[str]
    imagery: list[str]
    cultural_notes: list[str]
    tone: str

def call_pplx(messages: list[dict], system: str | None = None, temperature: float = 0.35, max_tokens: int = 700) -> dict:
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
    return {"service": "versequest-backend", "status": "running"}

@app.post("/api/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    text = (req.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Missing text")
    text = text[:6000]

    system = (
        "You are a precise music-meaning analyst.\n"
        "Output MUST be ONLY a single valid JSON object with keys exactly:\n"
        '{ "song_credit": string[], "song_lyrics": string[], "meaning_lyrics": string[], "tldr": string, "themes": string[], "imagery": string[], "cultural_notes": string[], "tone": string }.\n'
        "Do not include Markdown, code fences, or any text before/after the JSON. No comments. No explanations."
    )
    user = f"""
        Analyze the following lyrics (language={req.lang}) and return ONLY JSON.
        If information is not found for a key, return an empty array [] for lists or an empty string "" for strings.

        song_credit: ["Song Name:...", "Singer:...", "Movie/Album:..."].
        song_lyrics: find Full lyrics, each line as a separate string in the array.
        meaning_lyrics: write meaning of the song Line-by-line while mainting the poetinc feel, each line as a string.
        tldr: One-sentence plain summary.
        themes: Array of 3-6 theme strings.
        imagery: Array of 3-6 imagery/metaphor strings.
        cultural_notes: Array of 1-5 cultural reference strings.
        tone: A short string (e.g., "melancholic, rebellious").

        Lyrics:
        {text}
        """.strip()

    data = call_pplx(
        messages=[{"role": "user", "content": user}],
        system=system,
        temperature=0.35,
        max_tokens=800, # Increased slightly for longer lyrics
    )

    content = ""
    try:
        content = data.get("choices", [])[0].get("message", {}).get("content", "")
    except (IndexError, AttributeError) as e:
        print(f"Error extracting content: {e}")

    print("RAW AI CONTENT (first 200 chars):", content[:200])

    parsed = {}
    try:
        # ** FIX: Robustly find and parse the JSON block **
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = content[json_start:json_end]
            parsed = json.loads(json_str)
        else:
            raise ValueError("No JSON object found in AI response.")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing failed: {e}. Falling back.")
        # Fallback if parsing fails
        parsed = {
            "song_credit": [], "song_lyrics": [], "meaning_lyrics": [],
            "tldr": f"Could not parse the AI's response. Raw output: {content[:500]}",
            "themes": [], "imagery": [], "cultural_notes": [], "tone": "unknown",
        }

    # Normalize and enforce types to be safe
    def ensure_list_str(key):
        val = parsed.get(key, [])
        return [str(item) for item in val] if isinstance(val, list) else [str(val)]

    def ensure_str(key, default=""):
        return str(parsed.get(key, default))

    # Create the final, clean payload
    final_payload = {
        "song_credit": ensure_list_str("song_credit"),
        "original_lyrics": ensure_list_str("song_lyrics"), # Map song_lyrics to original_lyrics
        "meaning_lyrics": ensure_list_str("meaning_lyrics"),
        "tldr": ensure_str("tldr"),
        "themes": ensure_list_str("themes"),
        "imagery": ensure_list_str("imagery"),
        "cultural_notes": ensure_list_str("cultural_notes"),
        "tone": ensure_str("tone", "neutral"),
    }

    return ExplainResponse(**final_payload)
