import asyncio
import os
import json
import redis.asyncio as redis
from services.database import create_pool
from services.events import batch_insert_events

async def run_worker():
    # Get config from environment
    redis_host = os.getenv("REDIS_HOST", "localhost")
    print(f"🚀 Worker starting. Connecting to Redis at {redis_host}...")
    
    # Initialize connections
    pool = await create_pool()
    r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    
    try:
        while True:
            # Fetch up to 100 events from the queue
            batch = []
            for _ in range(100):
                item = await r.lpop("event_queue")
                if item:
                    batch.append(item)
                else:
                    break
            
            if batch:
                print(f"📦 Processing batch of {len(batch)} events...")
                await batch_insert_events(pool, batch)
                print("✅ Batch inserted to Supabase.")
            
            
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"❌ Worker Error: {e}")
    finally:
        await pool.close()
        await r.close()

if __name__ == "__main__":
    asyncio.run(run_worker())