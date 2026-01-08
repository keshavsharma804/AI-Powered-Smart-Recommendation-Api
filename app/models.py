from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: int
    title: str
    tags: List[str] = []

class RecommendRequest(BaseModel):
    query: str
    products: List[Product]

class RecommendationResult(BaseModel):
    id: int
    score: float
    reason: str

class RecommendResponse(BaseModel):
    recommendations: List[RecommendationResult]
