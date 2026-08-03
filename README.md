# PulseTrack — High-Throughput Analytics SaaS Platform

PulseTrack is a high-performance, distributed event ingestion engine designed to handle massive traffic surges using an asynchronous producer-consumer architecture.

## System Architecture
Unlike traditional synchronous logging, PulseTrack decouples data ingestion from storage to ensure zero latency for the end-user and maximum fault tolerance.

1. **Ingestion Layer (FastAPI):** A high-speed entry point that validates `x-api-key` headers and offloads event payloads to a message broker.
2. **Buffering Layer (Redis):** Acts as a shock absorber, preventing database bottlenecks during peak traffic surges.
3. **Processing Layer (Python/Asyncio):** A background worker that pulls batches from Redis and performs optimized bulk-inserts into the database.
4. **Persistence Layer (PostgreSQL/Supabase):** Stores structured event data and metadata for long-term analysis.
5. **Visualization Layer (Next.js):** A premium, glassmorphism-style dashboard providing real-time activity metrics and event distribution insights.

##  The Tech Stack
- **Backend:** Python, FastAPI, Redis, Asyncpg
- **Frontend:** Next.js, TypeScript, Recharts, Lucide Icons
- **DevOps:** Docker (Local Redis & Service Orchestration)
- **Database:** Supabase (PostgreSQL)

##  Key Features
- **Asynchronous Ingestion:** Returns `202 Accepted` instantly to the client while processing happens in the background.
- **Batched Persistence:** Minimizes database I/O by grouping events before insertion.
- **Secure Access:** Per-application API key validation.
- **Premium Analytics UI:** Apple Vision Pro-inspired aesthetic with dynamic time-series filtering (24h / 7d / 30d).

##  Getting Started

### 1. Boot the Backend Infrastructure
Ensure Docker is running on your machine, then spin up the message broker and backend services:

```bash
# Start the Redis message broker
docker run -d --name redis-local -p 6379:6379 redis:7-alpine

# In a new terminal, start the Ingestion API
PYTHONPATH=. fastapi dev services/ingestion-api/main.py

# In another terminal, start the Background Worker
PYTHONPATH=. python services/worker/worker.py
2. Run the Frontend Dashboard
Navigate to the Next.js client and start the UI:

Bash
cd frontend
npm install
npm run dev
📈 Scalability Roadmap
Horizontal Scaling: Deploy via Kubernetes to scale workers based on Redis queue depth.

Persistence Upgrades: Migrate to ClickHouse for billion-row analytical performance.

Global Distribution: Use Edge Functions for ingestion closer to the user.
