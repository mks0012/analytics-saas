import os
import json
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

# Internal Imports
from services.database import create_pool

VALID_API_KEYS = {"test_key", "dev_key_999", "manoj_prod_abc"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup shared resources
    redis_host = os.getenv("REDIS_HOST", "localhost")
    app.state.pool = await create_pool()
    app.state.redis = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    print(f"🚀 API Startup Complete. Redis: {redis_host}")
    yield
   
    if app.state.pool:
        await app.state.pool.close()
    if app.state.redis:
        await app.state.redis.close()

app = FastAPI(lifespan=lifespan)

# CORS configuration to allow local frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyticsEvent(BaseModel):
    event_name: str
    metadata: Optional[Dict[str, Any]] = {}

@app.post("/v1/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_event(event: AnalyticsEvent, x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    event_data = {
        "event_name": event.event_name, 
        "metadata": event.metadata, 
        "api_key": x_api_key
    }
    
    # Push to Redis
    await app.state.redis.rpush("event_queue", json.dumps(event_data))
    return {"status": "accepted"}

@app.get("/v1/analytics/summary")
async def get_summary(days: int = 1):
    if not app.state.pool:
        raise HTTPException(status_code=500, detail="Database connection missing")
    
    async with app.state.pool.acquire() as conn:
        # Time-based filtering logic
        start_time = datetime.utcnow() - timedelta(days=days)
        
        query = """
            SELECT event_name, COUNT(*) as count 
            FROM events 
            WHERE created_at >= $1 
            GROUP BY event_name
        """
        rows = await conn.fetch(query, start_time)
        breakdown = [dict(row) for row in rows]
        total = sum(item['count'] for item in breakdown)
        
        return {
            "total_events": total,
            "breakdown": breakdown
        }

@app.delete("/v1/analytics/clear")
async def clear_data():
    async with app.state.pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE events")
        return {"status": "success", "message": "All data cleared"}