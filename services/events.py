import asyncpg
import json
from typing import List

async def batch_insert_events(pool: asyncpg.Pool, events_batch: List[str]):
    if not events_batch:
        return

    # Convert the raw text from Redis back into Python data
    parsed_events = [json.loads(event) for event in events_batch]
    
    async with pool.acquire() as connection:
        async with connection.transaction():
            # This is the SQL command. 
            # Check TablePlus: if your column is called 'tenant_id', change 'api_key' to 'tenant_id'
            query = """
                INSERT INTO events (api_key, event_name, metadata)
                VALUES ($1, $2, $3)
            """
            
            values = [
                (
                    e.get("api_key"), 
                    e.get("event_name"), 
                    json.dumps(e.get("metadata")) 
                ) 
                for e in parsed_events
            ]
            
            await connection.executemany(query, values)