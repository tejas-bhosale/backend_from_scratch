# 26 Sundays — the weekly schedule and how to actually run it

Companion to `claude/backend-fundamentals-plan.md`. That doc says *what* to build. This one says *when*, *how*, and *what to read*.

**Window:** Wed 16 Sep 2026 → Sun 14 Mar 2027 · ~6.5 hrs/week · **two slip weeks remaining.**

> **Restart log**
> — *7–15 Sep 2026:* original week 1 passed with no work done. Counted as slip #1 of 3. Whole schedule shifted right by seven days; end date moved from 7 Mar to 14 Mar 2027. Nothing was cut.

---

## 0. The restart week (Wed 16 – Sun 20 Sep)

Starting cold is harder than continuing, so week 1 is deliberately smaller than the weeks that follow. Two changes for the first fortnight only:

- **No DSA yet.** The daily 30 minutes starts in week 3, once the build habit exists. Two habits at once is how both die.
- **Tonight replaces the Sunday reset.** Fifteen minutes, before you sleep: `mkdir backend-from-scratch/00-sockets`, `git init`, and write one line in NOTES.md — *"What does the kernel actually hand me when I call socket()?"* That's the whole task. Nothing else.

**Tomorrow, Wed 16 Sep, 60 minutes, cold attempt.** No reading, no tutorials, no searching. Open an editor and try to write a TCP server that accepts one connection and echoes back what it receives. You will get stuck. When you do, write the specific thing you got stuck on into NOTES.md and stop. Getting stuck *is* the deliverable — it is what makes Thursday's reading useful.

The bar for this week is one file that runs and one paragraph. That's it.

---

## 1. The week: one loop, four kinds of session

The single most common way this fails is opening a tutorial during a build session. Attempting, reading, building and explaining are different activities that reward different states of mind. Give each its own slot and protect the boundaries.

| When | Length | Session | What happens |
|---|---|---|---|
| Sun evening | 15 min | **Set the question** | Write one question you cannot currently answer into the repo. Not a topic — a question with a done condition. |
| Tue night | 60 min | **Cold attempt** | No reading. Open an editor and fail at it. Log every specific thing you got stuck on. |
| Thu night | 60 min | **Targeted read** | Read only enough to answer what you wrote down. Docs and source. Close the tab when the question is answered. |
| Sat or Sun | 3–4 h | **The build block** | Uninterrupted, phone elsewhere. First 20 min re-reading last week's notes; last 30 min taking the measurement. |
| Sun evening | 45 min | **Write the mechanism** | Explain it in your own words, commit, and turn whatever you hedged on into next week's question. |

**6 h 30 min committed.** Plus 30 min of DSA each morning from week 3 — a separate habit that never eats this budget.

## 2. How to run a session

1. **One repo, one directory per layer, a commit every session.** `backend-from-scratch/00-sockets/` … `08-operations/`. Commit even when it's broken — `git log` becomes the evidence that six months happened.
2. **Every layer has a NOTES.md with three headings:** *The question · What surprised me · What I still can't explain.* The third heading is the most valuable thing you write all week.
3. **End every session by writing the next session's first command.** One line at the bottom of NOTES.md. Restart cost is what kills evening sessions; this removes it.
4. **Stuck for 45 minutes? Read source, not tutorials.** CPython's `socketserver`, Werkzeug, redis-py, the Postgres docs.
5. **A week is done when it produced three things: a commit, a number, and a paragraph.** Missing the number means you built a demo; missing the paragraph means you don't yet know what you built.
6. **Timebox at 1.5×, then ship it ugly.** Perfectionism is tutorial hell wearing a different outfit.

## 3. Slip protocol — two left

Six months will contain a bad sprint at work, a festival week, and something unpredictable. A plan that assumes otherwise breaks on first contact.

- **Declare a slip on Sunday, not Thursday.** A declared slip costs one week. An undeclared one — the week that quietly evaporates and then feels too heavy to restart — costs the habit. That is exactly what the first week cost.
- **The recovery rule: never restart on a Monday.** Restart on the next day that exists. A plan you resume on a Wednesday is a plan; a plan that waits for a clean Monday is a wish.
- **On a slip week, do the 30-minute DSA anyway** (once it's running, from week 3). The daily habit keeps the streak alive while the big block is gone.
- **Week 16 is pre-declared light** (28 Dec – 3 Jan) — reading only. It is freely swappable with week 15 if the Christmas week is the one that gets eaten.
- **Two slips left means finishing late March instead of mid-March.** 26 real weeks in 28 calendar weeks is a success; 26 shallow weeks on time is not.

---

## 4. The 26 weeks

### September 2026 — layers 00–01, sockets and HTTP

**W1 · Sep 16–20 — "What does the kernel actually hand me when I call `socket()`?"** *(restart week — see §0)*
Build: TCP echo server in ~40 lines — bind, listen, accept, recv, send. Connect with `telnet` and a Python client. Kill the server mid-connection and see what the client gets.
Ship: `00-sockets/echo_server.py` + NOTES.md answering the question in your own words.

**W2 · Sep 21–27 — "Where does a request's time actually go?"**
Build: `strace -f` the echo server, name every syscall for one request. Then `curl -v --trace-time` against three real APIs and split the cost into DNS / TCP / TLS / TTFB.
Ship: `00-sockets/SYSCALLS.md` — annotated trace + three timing breakdowns.

**W3 · Sep 28–Oct 4 — "What is the minimum a server must do before a browser is satisfied?"**
Build: parse the request line and headers by hand; serve static files with correct `Content-Length`. Then set it wrong on purpose and watch Chrome hang — that hang is the lesson.
Ship: `01-http/server_v1.py` serving a real HTML page in a real browser. **DSA daily habit starts this week.**

### October 2026 — layers 01–02, concurrency models and the framework

**W4 · Oct 5–11 — "How many connections can one process hold at once, and what decides it?"**
Build: the same server three ways — thread-per-connection, fixed thread pool, single-threaded `selectors` event loop.
Ship: three variants that all pass one shared test script.

**W5 · Oct 12–18 — "Where exactly does each concurrency model break?"**
Build: `wrk` or `hey` against all three at 10 / 100 / 1000 concurrent connections — once with an instant handler, once with a 200 ms sleep. Plot throughput and p99.
Ship: `01-http/BENCHMARK.md` with the chart and why the curves cross. **Layer 00–01 README.**

**W6 · Oct 19–25 — "What is a web framework, minus the thirty thousand lines of edge cases?"**
Build: router with typed path params (`/users/<int:id>`), a middleware stack that wraps handlers, JSON parsing with validation, structured error contract.
Ship: `02-framework/` running a five-endpoint demo app.

**W7 · Oct 26–Nov 1 — "What is the contract between a server and an application?"**
Build: make the framework WSGI-compliant (PEP 3333), run the same app unchanged under gunicorn. Then read Flask and Werkzeug and write down three places they're smarter than you.
Ship: Layer 02 README + **HLD writeup #1** — a URL shortener where you justify the storage engine, not just the hash.

### November 2026 — layer 03, storage engines and query plans

**W8 · Nov 2–8 — "What does a single write physically cost?"**
Build: Bitcask-style KV store — appends to a log file, in-memory dict maps key → offset, reads seek. Measure writes/sec with `fsync` on and off.
Ship: `03-storage/kv/` plus the two numbers and what they cost.

**W9 · Nov 9–15 — "How does a database survive being killed mid-write?"** *(festival season — first slip candidate)*
Build: crash recovery by replaying the log on startup. Then compaction, and tombstones so deletes reclaim space.
Ship: a test that `kill -9`s the process mid-write and comes back consistent.

**W10 · Nov 16–22 — "Why is this query slow, and how would I know without guessing?"**
Build: five million rows into Postgres. Read `EXPLAIN ANALYZE` *before* changing anything. Add an index, re-read the plan, measure. Then find a query the index doesn't help and explain why not.
Ship: `03-storage/INDEX_LAB.md` — five query plans, before and after, with timings.

**W11 · Nov 23–29 — "What schema makes a bad state impossible rather than merely unlikely?"**
Build: model orders, line items, payments, refunds with constraints that reject nonsense. Then write the six queries that hurt: multi-table joins, aggregation, window functions, a recursive CTE.
Ship: `schema.sql` + `queries.sql` + **Layer 03 README.**

### December 2026 — layers 04–05, transactions and concurrency

**W12 · Nov 30–Dec 6 — "Which concurrency anomaly is my code exposed to right now?"**
Build: two `psql` windows side by side. Reproduce a lost update, a write skew and a deadlock on purpose. Fix each three ways — higher isolation, `SELECT … FOR UPDATE`, an atomic `UPDATE` — and argue which is right.
Ship: `04-transactions/ANOMALIES.md` with the exact SQL to reproduce each.

**W13 · Dec 7–13 — "What SQL is my ORM actually sending, and when?"**
Build: a ~200-line ORM over `psycopg` — model base class, chainable query builder, lazy relationships. Create an N+1 on purpose, watch it in the query log, fix with eager loading you wrote.
Ship: the ORM + **HLD writeup #2** (a ledger whose balances are provably correct). At work: find where ActiveRecord opens and commits a transaction in SequenceBase.

**W14 · Dec 14–20 — "What is `await` actually doing while it waits?"**
Build: an event loop over `selectors` that runs generator-based coroutines and can await a socket read. Write your own `run_until_complete`.
Ship: your loop running two concurrent fetches. **Start DDIA, ch. 1–4.**

**W15 · Dec 21–27 — "Threads, processes, or async — and how would I prove it?"**
Build: LRU cache with TTL. Break it with 50 threads, fix with a lock, measure contention, fix better with sharded locks. Then benchmark threads vs processes vs asyncio, once CPU-bound and once I/O-bound.
Ship: `05-concurrency/FOUR_NUMBERS.md` + Layer 05 README. *(Swap with W16 if this is the holiday week that disappears.)*

**W16 · Dec 28–Jan 3 — "What does at-least-once delivery actually cost me?"** *(pre-declared light week)*
Read only: DDIA ch. 5–7, Brandur Leach on job queues and idempotency. No build block required.
Ship: a page on why exactly-once delivery is a marketing term.

### January 2027 — layers 06–07, queues, caches, API contracts

**W17 · Jan 4–10 — "What happens to a job when its worker dies halfway through?"**
Build: queue on Postgres with `SELECT … FOR UPDATE SKIP LOCKED` — enqueue, claim, ack, retry with exponential backoff and jitter, DLQ after N attempts, worker pool. Then `kill -9` a worker mid-job and make sure the job comes back.
Ship: `06-queue/` with a test proving nothing is lost on a hard kill.

**W18 · Jan 11–17 — "What makes a consumer genuinely idempotent, and what makes a cache dangerous?"**
Build: the same queue interface on Redis — then name the durability trade you just made. Make a consumer idempotent and prove it by delivering every message twice. Then expire 10,000 cache keys at once, watch the stampede hit Postgres, and fix it.
Ship: Layer 06 README. **DDIA ch. 8–9.**

**W19 · Jan 18–24 — "What happens when a client retries a request that already succeeded?"**
Build: transfers with idempotency keys — same key twice returns the first result and never moves money twice. Handle simultaneous arrival.
Ship: `07-api/` with a concurrent test firing the same key from ten threads.

**W20 · Jan 25–31 — "How do I enforce a limit atomically across many app servers?"**
Build: token-bucket rate limiter as a single atomic Redis Lua script, then a sliding-window version, then a paragraph on when each is right. Plus cursor pagination that stays correct while rows are inserted underneath it.
Ship: the limiter + **HLD writeup #3** — a rate-limited multi-tenant API.

### February 2027 — layers 07–08, auth, observability, operations

**W21 · Feb 1–7 — "What does a token's signature prove, and what does it not?"**
Build: Argon2 password hashing. Sign and verify a JWT by hand with `hmac` before importing a library. Then attack your own verifier: `alg=none`, expired token, tampered claim.
Ship: Layer 07 README including the three attacks and why each failed.

**W22 · Feb 8–14 — "Could I debug this service with no access to the code?"**
Build: structured JSON logs with a request ID threaded end to end. Prometheus latency histograms. One Grafana dashboard you'd actually open during an incident. OpenTelemetry traces API → queue → worker → DB.
Ship: a dashboard screenshot and one span you didn't expect to be slow. **DDIA ch. 10–12.**

**W23 · Feb 15–21 — "What does my service do while it is dying?"**
Build: graceful shutdown on SIGTERM — stop accepting, drain in-flight jobs, exit clean — proven under load. Containerize, put nginx in front, add timeouts and a circuit breaker on the one external call. Load-test until something breaks.
Ship: a one-page incident note written as if real. **Mock system design interview #1.**

**W24 · Feb 22–28 — "Can I design the whole thing on paper before writing any of it?"**
Build: the consolidation service — a small payments or inventory API using all nine layers. This week is design doc and skeleton only: endpoints, schema, failure modes, trade-offs. README first, then code.
Ship: a design doc you'd defend in an interview, plus a running skeleton.

### March 2027 — consolidation

**W25 · Mar 1–7 — "Does it survive everything I now know how to break?"**
Build: real Postgres with the right constraints, the worker queue, idempotent endpoints, a proper test suite including the concurrency cases from weeks 12 and 19.
Ship: a green suite with at least three tests a normal project wouldn't have.

**W26 · Mar 8–14 — "Can I explain every trade-off I made, without hedging?"**
Build: instrument it, deploy it, load-test it, write the trade-offs README — every decision, the alternative rejected, and why.
Ship: the deployed service. Rewrite the resume around what you built. **Mock interviews #2 and #3.**

---

## 5. Once a month — the review that keeps you honest

Last Sunday of each month, spend 90 minutes of the build block on this instead.

- **Re-answer the diagnostic questions for every finished layer.** Out loud, cold, no notes. If you can't, you moved too fast — the fix is one focused week, not starting over.
- **Write one HLD document**, drawn from the layer you just built. Weeks 7, 13 and 20 have the specific prompts.
- **Update the résumé line for the month** — one sentence naming what you built and the number you measured. Six of these become the strongest section of your CV, and they're impossible to write retroactively.
- **Check the DSA streak, not the DSA count.** A 30-day streak of one problem beats a weekend of twenty.

---

## 6. Resources — in this order, at these moments

Short on purpose. Almost everything is free, a primary source, or a book you read once and return to for years. No video courses, because a video course is the exact shape of tutorial hell.

### Layers 00–01 (weeks 1–5)
- **Beej's Guide to Network Programming** *(free)* — the canonical sockets tutorial. It's in C, and that's the point. <https://beej.us/guide/bgnet/>
- **High Performance Browser Networking**, Grigorik *(free)* — TCP, TLS and HTTP/2 chapters. <https://hpbn.co/>
- **"Let's Build A Web Server"**, Ruslan Spivak *(free)* — three parts, builds exactly what week 3 asks for, in Python. Read *after* your cold attempt.
- **Julia Evans' blog and zines** — best writing anywhere on `strace`, networking, containers. <https://jvns.ca/>
- **RFC 9110 and MDN's HTTP reference** *(free)* — primary sources; look things up here, not in blog posts.

### Layer 02 (weeks 6–7)
- **PEP 3333, the WSGI spec** *(free)* — short, readable, and it's the contract you're implementing.
- **Flask and Werkzeug source** *(free)* — small enough to read end to end; Werkzeug's routing module is the one to study.
- **FastAPI docs on dependency injection** *(free)* — unusually good writing on a pattern you'll want in your own framework.

### Layers 03–04 (weeks 8–13)
- **Use The Index, Luke!**, Markus Winand *(free)* — the best explanation of B-tree indexes in existence; answers week 10 directly. <https://use-the-index-luke.com/>
- **Database Internals**, Alex Petrov — ch. 2–4 while building the KV store. It's describing what you're writing.
- **The Bitcask paper** *(free)* — fifteen pages; it is the entire design for week 8.
- **PostgreSQL docs, MVCC and Indexes chapters** *(free)* — source of truth for weeks 10–12.
- **`explain.depesz.com`** *(free)* — paste a plan, see where the time went.

### Layer 05 (weeks 14–15)
- **David Beazley, "Understanding the Python GIL"** *(free)* — the one talk worth watching in six months; answers week 15 with live benchmarks.
- **"A Web Crawler With asyncio Coroutines"**, *500 Lines or Less* *(free)* — builds an event loop from scratch. Exactly week 14.
- **CPython's `selectors` and `asyncio` source** *(free)* — read `base_events.py` after writing your own loop.

### Layers 06–07 (weeks 16–21)
- **Designing Data-Intensive Applications**, Kleppmann — the spine. Start week 14, not before.
- **Brandur Leach's articles** *(free)* — idempotency keys, transactional outbox, Postgres job queues, by someone who shipped them at Stripe. <https://brandur.org/articles>
- **Stripe's API docs and idempotency guide** *(free)* — read as a specimen of API design; it's the standard you're designing against in week 19.
- **OWASP Cheat Sheet Series** *(free)* — authentication, session management, password storage. Your week-21 attack list comes from here.

### Layer 08 (weeks 22–23)
- **Release It!**, Michael Nygard — timeouts, circuit breakers, bulkheads: the failure vocabulary for every interview.
- **Google SRE Book** *(free)* — monitoring, SLOs, postmortems. <https://sre.google/books/>
- **Liz Rice, "Containers From Scratch"** *(free)* — builds a container live in ~100 lines. After it, Docker stops being magic.
- **Prometheus and OpenTelemetry docs** *(free)* — specifically histogram vs summary, and why you cannot average a p99.

### Running alongside
- **Martin Kleppmann's Distributed Systems lecture series** *(free)* — Cambridge course on YouTube with published notes. The one video series that earns its place; watch during weeks 16–23 while the DDIA reading is live.
- **Build Your Own X** *(free)* — directory of from-scratch guides. Use it to find a second implementation to compare against, *after* writing yours.
- **CodeCrafters** *(paid)* — precisely your learning style: build your own Redis, HTTP server, SQLite or Git in Python, with tests. If a layer's build stalls, their track will unblock you.
- **NeetCode 150 / Blind 75** *(free)* — for the daily 30 minutes, from week 3. Work by pattern, not by list order.
- **System Design Interview vols 1 & 2**, Alex Xu — for interview *format* only, in the last two months. The mechanisms you'll explain come from the builds, not from here.