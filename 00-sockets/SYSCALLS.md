
# 10 here is NOT a port - it's the thread ID making this call. strace -f prefixes every line with which thread did it. 10 is the main thread (the one that calls accept4 in a loop).
10    <... futex resumed>)              = 0
11    recvfrom(4,  <unfinished ...>
# connection is being established here
10    accept4(3,  <unfinished ...>
# two different things happen here, don't mix them up: (1) a NEW THREAD, 11, gets spawned to handle this one client (threading.Thread in the Python code) - 11 is a thread ID, not a port. (2) inside that thread, accept4 hands back a NEW FD, 4, which is the actual connection object - that's what every recvfrom(4,...)/sendto(4,...) below refers to. Thread 10 (not 11) is the one that goes back to searching for new connections - it loops on accept4 forever; thread 11 only ever talks to this one client.
11    <... recvfrom resumed>"how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
# here recvfrom tells kernel to receive payload and give to it. i am not sure about what 4 indicates, 1024 is max byte size we are accepting. "how cool" is actual text that is received. 8 is the total byte received 
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
# this trace is the SERVER's own syscalls, so sendto here is the server sending back to the CLIENT, not "to server"
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "how cool", 1024, 0, NULL, NULL) = 8
11    write(1, "[+] Recieved: b'how cool'\n", 26) = 26
11    sendto(4, "how cool", 8, 0, NULL, 0) = 8
11    recvfrom(4, "", 1024, 0, NULL, NULL) = 0
11    write(1, "[+] Recieved: b''\n", 18) = 18
11    close(4)                          = 0
11    rt_sigprocmask(SIG_BLOCK, ~[RT_1], NULL, 8) = 0
11    madvise(0xffff8aad0000, 8314880, MADV_DONTNEED) = 0
11    exit(0)                           = ?
11    +++ exited with 0 +++
# everything below is thread 10 (main thread) only - this is Ctrl+C. Thread 11 was already done and exited by this point (see above), so none of this touches it.

# thread 10 was blocked inside accept4, waiting for a new client. SIGINT arrives mid-call, so the kernel aborts the call with ERESTARTSYS instead of letting it finish normally
10    <... accept4 resumed>0xffffc2dbea58, [16], SOCK_CLOEXEC) = ? ERESTARTSYS (To be restarted if SA_RESTART is set)
# the actual signal delivery - the kernel records that SIGINT happened
10    --- SIGINT {si_signo=SIGINT, si_code=SI_KERNEL} ---
# the interrupted syscall formally fails here with EINTR ("interrupted system call") - this is what Python's socket code sees, and turns into a KeyboardInterrupt exception
10    rt_sigreturn({mask=[]})           = -1 EINTR (Interrupted system call)
10    write(2, "Traceback (most recent call last"..., 35) = 35
10    write(2, "  File \"/app/tcp-server.py\", lin"..., 50) = 50
# Python is now printing the traceback. To show the actual source line (not just the filename), it has to OPEN and READ my own script file again, live, off disk - that's why there's a whole open/read/close sequence (fd 4, then fd 5) just to print one line of context in the error message
10    openat(AT_FDCWD, "/app/tcp-server.py", O_RDONLY|O_CLOEXEC) = 4
10    fstat(4, {st_mode=S_IFREG|0644, st_size=1499, ...}) = 0
10    ioctl(4, TCGETS, 0xffffc2dbd920)  = -1 ENOSYS (Function not implemented)
10    lseek(4, 0, SEEK_CUR)             = 0
10    fcntl(4, F_DUPFD_CLOEXEC, 0)      = 5
10    fcntl(5, F_GETFL)                 = 0x20000 (flags O_RDONLY|O_LARGEFILE)
10    fstat(5, {st_mode=S_IFREG|0644, st_size=1499, ...}) = 0
10    read(5, "import socket \nimport threading "..., 4096) = 1499
10    close(5)                          = 0
10    lseek(4, 0, SEEK_SET)             = 0
10    read(4, "import socket \nimport threading "..., 8192) = 1499
10    close(4)                          = 0
10    write(2, "    client, addr = server.accept"..., 36) = 36
10    write(2, "  File \"/usr/local/lib/python3.1"..., 66) = 66
# same thing again, but this time it's reading CPython's own socket.py source, to show the frame inside accept() where the interrupt actually landed
10    openat(AT_FDCWD, "/usr/local/lib/python3.10/socket.py", O_RDONLY|O_CLOEXEC) = 4
10    fstat(4, {st_mode=S_IFREG|0644, st_size=37006, ...}) = 0
10    ioctl(4, TCGETS, 0xffffc2dbd920)  = -1 ENOTTY (Inappropriate ioctl for device)
10    lseek(4, 0, SEEK_CUR)             = 0
10    fcntl(4, F_DUPFD_CLOEXEC, 0)      = 5
10    fcntl(5, F_GETFL)                 = 0x20000 (flags O_RDONLY|O_LARGEFILE)
10    fstat(5, {st_mode=S_IFREG|0644, st_size=37006, ...}) = 0
10    read(5, "# Wrapper module for _socket, pr"..., 4096) = 4096
10    close(5)                          = 0
10    lseek(4, 0, SEEK_SET)             = 0
10    read(4, "# Wrapper module for _socket, pr"..., 8192) = 8192
10    read(4, "024] = \"Unrecognized QoS object."..., 8192) = 8192
10    close(4)                          = 0
10    write(2, "    fd, addr = self._accept()\n", 30) = 30
# the actual exception name finally gets printed
10    write(2, "KeyboardInterrupt\n", 18) = 18
# cleanup starts: Python restores SIGINT to its default OS behavior (it had installed its own handler to turn SIGINT into KeyboardInterrupt; that's done now, so it hands control back to the default)
10    rt_sigaction(SIGINT, {sa_handler=SIG_DFL, sa_mask=[], sa_flags=SA_ONSTACK}, {sa_handler=0xffff8ba02d88, sa_mask=[], sa_flags=SA_ONSTACK}, 8) = 0
# the interpreter is shutting down and garbage-collecting leftover objects - it checks this listening socket's own address (getsockname, fd 3) and tries to check its peer, which fails with ENOTCONN because a LISTENING socket was never connected to anyone - it's not a real connection, just a queue for incoming ones, so "who's my peer" has no answer
10    getsockname(3, {sa_family=AF_INET, sin_port=htons(9999), sin_addr=inet_addr("0.0.0.0")}, [16]) = 0
10    getpeername(3, 0xffffc2dbe8c8, [16]) = -1 ENOTCONN (Transport endpoint is not connected)
# the listening socket (fd 3, the one bound/listening since startup) finally gets closed as part of process teardown
10    close(3)                          = 0
10    munmap(0xffff8b4b1000, 151552)    = 0
10    rt_sigaction(SIGINT, {sa_handler=SIG_DFL, sa_mask=[], sa_flags=SA_ONSTACK}, {sa_handler=SIG_DFL, sa_mask=[], sa_flags=SA_ONSTACK}, 8) = 0
# now that SIGINT is back to its default behavior (not Python's custom handler), the process sends ITSELF a second SIGINT - and this time, since there's no handler left to turn it into a catchable exception, the OS's default action for SIGINT (terminate the process) actually runs
10    getpid()                          = 10
10    kill(10, SIGINT)                  = 0
10    --- SIGINT {si_signo=SIGINT, si_code=SI_USER, si_pid=10, si_uid=0} ---
10    +++ killed by SIGINT +++




Phase	google.com	api.github.com	httpbin.org
DNS	100.4 ms	164.9 ms	84.0 ms
TCP connect	17.0 ms	32.3 ms	304.6 ms
TLS handshake	139.7 ms	45.5 ms	589.8 ms
TTFB (server think time)	88.7 ms	39.6 ms	260.7 ms
Body download	37.7 ms	0.3 ms	0.5 ms
Total	383.4 ms	282.6 ms	1239.6 ms
