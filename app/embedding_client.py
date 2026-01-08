import requests
from .config import OPENROUTER_API_KEY, BASE_URL, EMBEDDING_MODEL

session = requests.Session()

session.headers.update({
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "Smart Recommendation API"
})

def get_embeddings(texts):
    payload = {
        "model": EMBEDDING_MODEL,
        "input": texts
    }

    resp = session.post(f"{BASE_URL}/embeddings",
                        json=payload,
                        timeout=20)

    resp.raise_for_status()

    return [d["embedding"] for d in resp.json()["data"]]
