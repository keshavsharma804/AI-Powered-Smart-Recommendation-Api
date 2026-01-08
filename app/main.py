from fastapi import FastAPI, HTTPException, Request
from .models import RecommendRequest, RecommendResponse
from .recommender import recommend
from .rate_limit import check_rate_limit
from .response_cache import (
    make_response_cache_key,
    get_cached_response,
    store_response
)
import time

app = FastAPI()


@app.post("/recommend/embeddings")
def api(payload: RecommendRequest, request: Request):

    user_key = request.client.host or "unknown"

    if not check_rate_limit(user_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    cache_key = make_response_cache_key(payload.query, payload.products)

    cached = get_cached_response(cache_key)
    if cached:
        return cached

    start = time.time()

    recs = recommend(payload.query, payload.products)

    latency = round((time.time() - start) * 1000)

    response = {"latency_ms": latency, "recommendations": recs}

   
    store_response(cache_key, response)

    return response





































