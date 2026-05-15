import asyncpg
from datetime import datetime, timedelta

async def get_total_events_24h(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        # Get count of events where created_at is within the last 24 hours
        query = """
            SELECT COUNT(*) 
            FROM events 
            WHERE created_at > NOW() - INTERVAL '24 hours'
        """
        count = await connection.fetchval(query)
        return count

async def get_event_breakdown(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        # Group by event_name to see what's most popular
        query = """
            SELECT event_name, COUNT(*) as count 
            FROM events 
            GROUP BY event_name 
            ORDER BY count DESC
        """
        rows = await connection.fetch(query)
        return [dict(row) for row in rows]