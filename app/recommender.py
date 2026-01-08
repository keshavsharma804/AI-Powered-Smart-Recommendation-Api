import hashlib
from .embedding_client import get_embeddings
from .similarity import cosine_similarity
from .cache import embedding_cache
import pickle
from .redis_client import redis_client

def build_text(product):
    title = str(product.title)
    tags = " ".join([str(t) for t in product.tags])
    return f"{title} {tags}".lower()


def explain(product, query):
    q_words = set(query.lower().split())
    title_words = set(product.title.lower().split())
    tag_words = set([t.lower() for t in product.tags])

    overlaps = sorted(q_words & (title_words | tag_words))

    if overlaps:
        return f"Matches query keywords: {', '.join(overlaps)}"

    return "High semantic similarity to the query"


def cache_key(text: str):
    return "emb:product:" + hashlib.sha256(text.encode("utf-8")).hexdigest()



def get_product_embedding(text: str):
    key = cache_key(text)

    
    if key in embedding_cache:
        return embedding_cache[key]

    cached = redis_client.get(key)
    if cached:
        emb = pickle.loads(cached)
        embedding_cache[key] = emb
        return emb

    emb = get_embeddings([text])[0]

 
    embedding_cache[key] = emb
    redis_client.set(key, pickle.dumps(emb))

    return emb

def recommend(query, products):
    try:
       
        query_emb = get_embeddings([query])[0]

        scored = []

        for p in products:
            text = build_text(p)
            emb = get_product_embedding(text)

            score = cosine_similarity(query_emb, emb)

            scored.append((p.id, float(score), explain(p, query)))

      
        scored.sort(key=lambda x: (-x[1], x[0]))

        top3 = scored[:3]

        return [
            {"id": p[0], "score": round(p[1], 4), "reason": p[2]}
            for p in top3
        ]

    except Exception as e:
        print("Embedding service failed — falling back to keyword match:", e)

        
        scored = []
        for p in products:
            s = keyword_score(query, p)
            scored.append((p.id, s))

        scored.sort(key=lambda x: (-x[1], x[0]))

        top3 = scored[:3]

        return [
            {"id": p[0], "score": p[1], "reason": "Keyword-based match fallback"}
            for p in top3
        ]



def keyword_score(query, product):
    q = set(query.lower().split())
    t = set(product.title.lower().split())
    tag = set([x.lower() for x in product.tags])
    return len(q & (t | tag))


def get_query_embedding(query: str):
    return get_embeddings([query])[0]
