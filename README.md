# ForgeLab: Ephemeral Production-Faithful Test Environments for Coding Agents

A local-first environment orchestrator that provides coding agents with production-shaped replicas—including copy-on-write PostgreSQL database clones, referential-integrity data anonymization, and HTTP dependency record/replay.

## Architecture

- **`backend/app/cloner/`**: Schema-and-data cloning engine with deterministic keyed pseudonymization preserving foreign key integrity and sub-second CoW replication.
- **`backend/app/proxy/`**: HTTP dependency recorder and replay proxy with header credential sanitization and programmable fault injection (latency, 500/504 errors).
- **`backend/app/provisioner/`**: Ephemeral environment orchestrator backed by a leak-proof watchdog with automatic teardown sweeps under agent termination.
- **`frontend/`**: Next.js 15 App Router environment console displaying replica launch progress, topology graphs, and live SSE log streams.
- **`benchmark/`**: `ForgeBench` 20 agent-generated patches (unsafe schema migrations, N+1 regressions, tenant leaks) asserting sub-second p95 cold-start and defect detection lift.

## Quick Start (Offline Verification)

```bash
# 1. Run backend unit tests (100% offline)
pytest backend/tests -v

# 2. Run ForgeBench 20-scenario benchmark
python3 benchmark/forge_bench.py
```

## Running Full Stack

```bash
# Start backend API (FastAPI)
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8004

# Start frontend (Next.js 15)
cd frontend && npm install && npm run dev
```
