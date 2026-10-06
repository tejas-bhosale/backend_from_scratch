# Layer 00 — the machine and the wire

## The question
What does the kernel actually hand me when I call `socket()`?

answer by me : i understood partially how socket works. Socket is a kernel managed objeect identified by protocol + IP address + Port. you create one, the os gives you back an integer description and you read/write to it much like a file. socket address is combination of ip address and port number. there are two types of sockets TCP and UDP. 

answer by llm :
- **File descriptor**: an index into a small per-process table the kernel keeps (`task_struct.files` on Linux). Each slot points to a kernel-side "open file" struct, which points to the real object — regular file, socket, pipe, etc. `socket()` doesn't hand you the object itself; it hands you the index. Every `read`/`write`/`close` you call with that integer is the kernel looking up that slot and acting on whatever it points to.
- **Why a socket is "treated as a file"**: Unix's core trick is that file descriptors are a uniform handle — the kernel doesn't care what's on the other end, only that the object implements a common interface (read, write, close, select/poll). A socket struct implements that interface just like a file struct does, so the same syscalls work on both. That's why `socket()` returns something that looks and behaves like a file descriptor: it is one, just pointing at a socket object instead of a file object.
- **How the OS creates/manages the object**: `socket()` triggers a syscall; the kernel allocates a `struct socket` (plus a `struct sock` holding the actual protocol state — TCP/UDP state machine, send/recv buffers), registers it internally, creates a file descriptor entry pointing at it, and returns the integer. From then on the socket only exists in kernel memory — the process just holds the integer key.

## What surprised me
That socket is not a physical connection and is object handled by OS.

## What I still can't explain
Istill dont know how it works in detailed manner. i am unable to understand how os creates an object and handles it. also i am not understanding that socket is treated as a file. I am not understanding what file descriptor is.

---
**Next session starts with:**


week 2:
## What i learned
I learned how server connection works. We mainly have two protocols TCP and UDP. These protocols have different way of connection. TCP is more reliable and makes sure that the message reaches the other server, while UDP does not gurantee that the message will reach the other server but is faster than TCP. I also leraned how connection is established for TCP using strace. Also lerned about what DNS time, TCP connect time, TLS handshake, TTFB (server think time), Body download

*(fix: "secure" → "reliable" - TCP guarantees delivery/ordering, it doesn't encrypt anything on its own; that's TLS's job, a separate layer on top. Also fixed the TCP/UDP swap in the second clause - it's UDP that doesn't guarantee delivery.)*

## What surprised me
lerning about how connection is actually established and seeing how after a connection a thread is created for said connection and how server goes back to listening for other connections.

## What I still can't explain
not sure about the TTFB and Body download time. Not sure about 4 in log "1    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8"

answer by llm:
- **TTFB (time to first byte)**: once DNS, TCP, and TLS are all done, your request has finally been sent. TTFB measures the gap between "request fully sent" and "first byte of the response arrives" - it's effectively how long the server's own code took to receive your request, do whatever work it needed to do (query a DB, run logic, etc.), and start writing a response back. A slow TTFB usually means a slow *server*, not a slow *network*.
- **Body download time**: after that first byte, the rest of the response still has to arrive - `total - ttfb` is how long it took to transfer the rest of the body over the already-open, already-encrypted connection. A large response or a slow/throttled connection shows up here, not in TTFB.
- **The `4` in `recvfrom(4, ...)`**: it's the file descriptor for this one client's connection - the number `accept()` handed back when this client connected (see `SYSCALLS.md`'s annotation on line 7 for where it's created). It's not a count or a size; it's the "claim-check" number the kernel uses internally to know which connection you're asking about. Every `recvfrom`/`sendto` call for this same client uses the same `4` because it's the same connection the whole time.
