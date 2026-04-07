from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
import redis
import json

app = FastAPI()


r = redis.Redis(host='localhost', port=6379, db=0)

class AnalyticsEvent(BaseModel):
    event_name: str
    metadata: Optional[Dict[str, Any]] = {}

@app.post("/v1/ingest")
async def ingest_event(event: AnalyticsEvent, x_api_key: str = Header(...)):
    
    event_data = {
        "event_name": event.event_name,
        "metadata": event.metadata,
        "api_key": x_api_key
    }

    
    r.lpush("event_queue", json.dumps(event_data))
    
    return {"status": "accepted", "message": "Event queued for processing"}