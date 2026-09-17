# Nine Layers Down — backend fundamentals plan

Interactive version: https://claude.ai/code/artifact/762dc881-3add-4ce2-959f-37a9f6092e09

**Context:** Tejas, ~5 yrs backend, career mostly in low-code (Frappe/ERPNext), now on a Rails codebase at Clarivate. Wants the mechanisms underneath the abstraction. Constraints chosen: **Python**, **5–8 hrs/week**, **build-from-scratch depth**, 26 weeks.

## The arithmetic (important)

26 weeks × ~6 hrs ≈ **160 hours**. HLD + LLD + distributed systems + DSA + Python backend + Gen AI do not fit in 160 hours at interview depth. Allocation:

- ~120 h — the nine layer builds
- ~20 h — one consolidation service (weeks 24–26)
- ~20 h — DDIA, read alongside from week 14
- DSA — 30 min daily, separate habit, outside this budget
- Gen AI — deferred to month 7+
- HLD — one design writeup per month, drawn from a layer just built
- LLD — practised inside the builds, not studied separately

## Diagnostic (answer cold, no lookups)

1. What is a socket, in terms of what the kernel gives your process?
2. What does gunicorn do that Flask does not?
3. A request takes 3s — how do you tell whether it was DNS, TCP, TLS, app, or DB?
4. Index on `(status, created_at)` — which queries use it, which can't?
5. Postgres default isolation level, and which anomaly it still allows?
6. Two requests read balance 100 and both write 90 — what went wrong, what's the fix?
7. Worker finishes the job, crashes before acking — what happens next?
8. 502 vs 504 — which one is your fault?
9. Why can more threads make a Python service slower?
10. What does a JWT signature prove, and not prove?
11. What does `docker run` ask the kernel to do?
12. Where does connection pooling live and why does it matter?

## The nine layers

**00 · The machine and the wire** (wk 1–2, ~12h) — processes/threads, file descriptors, syscalls, blocking I/O, TCP handshake, DNS, TLS, latency vs bandwidth.
*Build:* TCP echo server on raw sockets; `strace` one full request and name every syscall; `curl -v --trace-time` to separate DNS/TCP/TLS/response timings.

**01 · HTTP and the server loop** (wk 3–5, ~18h) — request/response anatomy, status semantics, keep-alive, Content-Length, chunked, HTTP/1.1 vs 2 vs 3, server concurrency models.
*Build:* your own HTTP server, parsing by hand; serve it thread-per-connection, thread-pool, and single-threaded `selectors` loop; load-test all three at 10/100/1000 concurrency and plot throughput + p99.

**02 · The framework you never wrote** (wk 6–7, ~12h) — routing, middleware chain, request context, WSGI/ASGI, serialization/validation, DI, error handling.
*Build:* ~300-line framework on top of layer 01, WSGI-compliant so the same app runs under gunicorn unchanged. Then read Flask/Werkzeug source and find three places they're smarter.

**03 · Storage engines and the shape of data** (wk 8–11, ~24h) — normalization, constraints, B-tree/composite/covering indexes, EXPLAIN ANALYZE, joins, window functions, WAL, fsync, compaction.
*Build:* Bitcask-style KV store (append-only log + in-memory offset index, fsync cost measured, crash recovery, compaction); a 5M-row Postgres index lab; a real schema where bad states are unrepresentable.

**04 · Transactions, isolation, and the lies ORMs tell** (wk 12–13, ~12h) — ACID, isolation levels, lost update, write skew, phantoms, MVCC, row locks, deadlocks, pooling, N+1.
*Build:* reproduce lost update / write skew / deadlock in two psql sessions and fix each three ways; a ~200-line ORM over psycopg with a deliberate N+1 you then fix.

**05 · Concurrency inside your own process** (wk 14–15, ~12h) — the GIL precisely, CPU vs I/O bound, event loop internals, coroutines, selectors/epoll, races, locks, backpressure.
*Build:* a 150-line event loop running generator coroutines; a thread-safe LRU+TTL cache broken under 50 threads then fixed with sharded locks; one benchmark across threads/processes/asyncio × CPU-bound/I/O-bound.

**06 · Queues, workers and caches** (wk 16–18, ~18h) — at-least-once vs at-most-once, ack/nack, visibility timeout, DLQ, retry with jitter, idempotent consumers, cache-aside, stampede, invalidation.
*Build:* job queue on Postgres `FOR UPDATE SKIP LOCKED` with retries/backoff/DLQ/worker pool, `kill -9` tested; same interface on Redis; a provably idempotent consumer; a cache stampede triggered then fixed.

**07 · API contracts and correctness under retry** (wk 19–21, ~18h) — resource modelling, idempotency keys, cursor vs offset pagination, versioning, error contracts, token bucket, sliding window, sessions vs JWT, OAuth2, password hashing.
*Build:* payments-shaped API — idempotency keys incl. the simultaneous-arrival race; token-bucket limiter in Redis Lua; cursor pagination correct under concurrent inserts; Argon2 + hand-rolled HMAC JWT, then break it (alg=none, expired, tampered).

**08 · Running it** (wk 22–23, ~12h) — structured logging, RED/USE metrics, histograms/p99, tracing, health vs readiness, SIGTERM drain, namespaces/cgroups, reverse proxy, 12-factor, timeouts, circuit breakers.
*Build:* instrument the queue service — JSON logs with request IDs, Prometheus histograms, one real Grafana dashboard, OTel traces API→queue→worker→DB, graceful shutdown proven under load, containerized behind nginx, load-tested to breaking with a written incident note.

**Weeks 24–26 · consolidation service** — one small payments or inventory API using all nine layers: real Postgres, worker queue, idempotent endpoints, metrics, traces, graceful shutdown, and a README explaining every trade-off. This is the artefact that changes interviews.

## Anti-tutorial-hell rules

1. Write the failing version first — attempt every build cold before reading anything.
2. Stuck an hour → read source (CPython socketserver, Werkzeug, redis-py, Postgres docs, RFC 9110), not tutorials.
3. Every build ends with one measurement: a benchmark, query plan, trace, or p99.
4. Write a README explaining the mechanism in your own words. Where you hedge is the gap.
5. No new layer until the last one is explained. Nine finished builds beat twenty abandoned repos.
6. Timebox at 1.5× budget, then ship it ugly.

## Reading (in this order, at these times)

- **DDIA** — Kleppmann. Start week 14, not before.
- **Database Internals** — Petrov, ch. 2–4, while building the KV store.
- **High Performance Browser Networking** — Grigorik (free), TCP/TLS/HTTP2 chapters during layers 00–01.
- **Release It!** — Nygard, for layer 08.
- **Postgres docs**, MVCC and index chapters — source of truth for layers 03–04.
- **Source**: Flask + Werkzeug, redis-py, Python's `socketserver` — after writing your own version, never before.