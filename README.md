# Python Concurrency and Parallelism Demonstration

This repository provides a practical example of how concurrency and parallelism work in Python. The code compares sequential execution with threaded and multi-process execution for both CPU-bound and I/O-bound tasks.

## Key Concepts

### Global Interpreter Lock (GIL)
- **What is the GIL?**  
  The GIL is a mechanism in CPython that allows only one thread at a time to execute Python bytecode. While it simplifies memory management and garbage collection, it also limits true parallelism in CPU-bound tasks when using threads.

### CPU-bound vs I/O-bound
- **CPU-bound tasks:**  
  These are tasks that spend most of their time using the CPU (e.g., complex mathematical computations). Due to the GIL, multiple threads won't run CPU-bound Python code in parallel effectively.  
  **Solution:** Use multiple processes, as each process has its own GIL and can run truly in parallel on separate CPU cores.

- **I/O-bound tasks:**  
  These tasks often wait for external operations like network calls, disk reads/writes, or user input. While one thread is waiting, another can run, so threads can improve performance significantly here even with the GIL.  
  **Solution:** Threads or asynchronous I/O (e.g., `asyncio`) can be very effective for I/O-bound tasks.

### Threads vs Processes
- **Threads:**  
  Lighter weight, share the same memory space, but limited by the GIL for CPU-bound operations.  
- **Processes:**  
  Heavier to create and manage, but each process runs its own interpreter and can achieve real parallelism on multiple CPU cores.

### Demonstrated Approaches in the Code
- **Sequential:**  
  Run tasks one after another.
- **ThreadPoolExecutor:**  
  Shows that CPU-bound tasks do not speed up due to the GIL, but I/O-bound tasks can be completed more efficiently.
- **ProcessPoolExecutor:**  
  Allows parallel execution for CPU-bound workloads by bypassing the GIL limit through multiple processes.

## Running the Code
Simply run:
```bash
python3 main.py
