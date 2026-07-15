import hashlib, json, os, sqlite3
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

DB = "results/llm_cache.sqlite"

def _db():
    Path("results").mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            model TEXT,
            request TEXT,
            response TEXT,
            prompt_tokens INT,
            completion_tokens INT,
            created TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn

def _key(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=60))
def _call_api(model: str, messages: list, temperature: float):
    return client.chat.completions.create(
        model=model, messages=messages, temperature=temperature
    )

def chat(model:str, messages:list, temperature: float = 0.0, run_tag: str = "") -> str:
    """Cached chat completion. run_tag lets you force distinct samples at the same temperature 
    (e.g. run_tag=`rep1`, `rep2` for stability runs)."""
    payload = {
        "model": model, 
        "messages": messages, 
        "temperature": temperature, 
        "run_tag": run_tag,
    }
    key = _key(payload)
    conn = _db()
    try:
        row = conn.execute("SELECT response FROM cache WHERE key=?", (key,)).fetchone()
        if row:
            return row[0]
        resp = _call_api(model, messages, temperature)
        text = resp.choices[0].message.content
        if not text:
            raise ValueError(f"empty response from {model}")   
        conn.execute("INSERT OR REPLACE INTO cache VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                    (key, model, json.dumps(payload), text, resp.usage.prompt_tokens, resp.usage.completion_tokens))
        conn.commit()
        return text
    finally:
        conn.close()

# prices in $ per 1M tokens: (input, output) — copied from openrouter.ai/models on 7/10/2026
PRICES = {
    "openai/gpt-4o-mini":          (0.15, 0.60),   
    "openai/gpt-4.1":              (2.00, 8.00),   
    "anthropic/claude-sonnet-4.5": (3.00, 15.00),  
    "google/gemini-2.5-flash":     (0.30, 2.50),
}

def spend_summary() -> float:
    conn = _db()
    try:
        rows = conn.execute("SELECT model, COUNT(*), SUM(prompt_tokens), SUM(completion_tokens) FROM cache GROUP BY model").fetchall()
        total = 0.0
        for model, n, pt, ct in rows:
            in_p, out_p = PRICES.get(model, (0, 0))
            cost = pt / 1e6 * in_p + ct / 1e6 * out_p
            total += cost
            print(f"{model}: {n} calls, {pt} in-tokens, {ct} out-tokens, ${cost:.4f}")
        print(f"TOTAL: ${total:.4f}")
        return total
    finally:
        conn.close()

def estimate_cost(pilot_fn, n_pilot: int, n_total: int) -> float:
    """pilot_fn() should execute your first n_pilot calls of the planned run."""
    before = spend_summary()
    pilot_fn()                      # e.g. grade the first 10 items
    after = spend_summary()
    per_call = (after - before) / n_pilot
    est = per_call * n_total

    print(f"~${per_call:.4f}/call -> estimated ${est:.2f} for {n_total} calls")
    return est

