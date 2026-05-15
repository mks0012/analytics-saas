import os
import asyncpg
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def get_db_config():
    """
    Determines the database host. 
    If running inside Docker, it uses the host provided by Docker Compose.
    Otherwise, it defaults to the Supabase host.
    """
    # Docker Compose will set DB_HOST to 'db' or 'localhost' 
    # but we want to prioritize the Supabase host for remote DB access.
    return {
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "postgres"),
        "host": os.getenv("DB_HOST", "db.woyfzzdogbadxbqwxiqs.supabase.co"),
        "port": os.getenv("DB_PORT", "5432")
    }

async def create_pool():
    config = get_db_config()
    try:
        pool = await asyncpg.create_pool(
            user=config["user"],
            password=config["password"],
            database=config["database"],
            host=config["host"],
            port=config["port"],
            min_size=5,
            max_size=20,
            # Supabase often requires SSL for remote connections
            ssl="require" 
        )
        print(f"✅ Connected to Database at {config['host']}")
        return pool
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        raise e