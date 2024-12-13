import time
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ------------------------------------------------------------
# Example functions
# ------------------------------------------------------------

# CPU-bound function: intensive computation (e.g., counting primes)
# This simulates a CPU-heavy task.
def count_primes(n):
    # Counts how many primes are there up to n.
    # This is a simple and unoptimized implementation, purely for demonstration.
    count = 0
    for num in range(2, n):
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            count += 1
    return count

# I/O-bound function: simulate I/O by sleeping
# This does not require heavy CPU usage, it just "waits" (like an I/O operation).
def simulate_io(duration):
    time.sleep(duration)
    return duration

# ------------------------------------------------------------
# Utility function to measure execution time
# ------------------------------------------------------------
def measure_time(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

# ------------------------------------------------------------
# Demonstration with CPU-bound tasks
# ------------------------------------------------------------
def demo_cpu_bound():
    print("\n--- CPU-bound Demonstration ---")
    # We will use a reasonably large N to simulate a CPU-intensive task.
    N = 50_000
    times_to_run = 4  # run the function multiple times

    # Sequential execution
    def run_sequential():
        return [count_primes(N) for _ in range(times_to_run)]

    _, seq_time = measure_time(run_sequential)
    print(f"Sequential (CPU-bound): {seq_time:.2f} s")

    # Using ThreadPoolExecutor
    # Due to the GIL, threads won't provide real parallelism for CPU-bound tasks.
    def run_with_threads():
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(count_primes, N) for _ in range(times_to_run)]
            return [f.result() for f in futures]

    _, thread_time = measure_time(run_with_threads)
    print(f"Threads (CPU-bound): {thread_time:.2f} s")
    print("Note that for CPU-bound tasks, threads usually do not improve performance due to the GIL.")

    # Using ProcessPoolExecutor
    # Processes have their own GIL and separate memory space, allowing true parallelism.
    def run_with_processes():
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(count_primes, N) for _ in range(times_to_run)]
            return [f.result() for f in futures]

    _, process_time = measure_time(run_with_processes)
    print(f"Processes (CPU-bound): {process_time:.2f} s")
    print("With processes, we expect to see performance improvement compared to threads in CPU-bound scenarios.")

# ------------------------------------------------------------
# Demonstration with I/O-bound tasks
# ------------------------------------------------------------
def demo_io_bound():
    print("\n--- I/O-bound Demonstration ---")
    # Simulate I/O by sleeping.
    # Let's say we have 4 tasks that each sleep for 1 second.
    times_to_run = 4
    delay = 1

    # Sequential execution
    def run_sequential():
        return [simulate_io(delay) for _ in range(times_to_run)]

    _, seq_time = measure_time(run_sequential)
    print(f"Sequential (I/O-bound): {seq_time:.2f} s")

    # Using Threads
    # For I/O-bound tasks, threads can improve performance since while one thread is waiting,
    # others can proceed.
    def run_with_threads():
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(simulate_io, delay) for _ in range(times_to_run)]
            return [f.result() for f in futures]

    _, thread_time = measure_time(run_with_threads)
    print(f"Threads (I/O-bound): {thread_time:.2f} s")
    print("For I/O-bound tasks, threads often provide a significant performance benefit.")

    # Using Processes for I/O-bound
    # Processes can also help, but have more overhead compared to threads.
    def run_with_processes():
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(simulate_io, delay) for _ in range(times_to_run)]
            return [f.result() for f in futures]

    _, process_time = measure_time(run_with_processes)
    print(f"Processes (I/O-bound): {process_time:.2f} s")
    print("Processes can also parallelize I/O, but due to overhead, the gain might not be as large as with threads.")

if __name__ == "__main__":
    # Demonstrating the difference between CPU-bound and I/O-bound tasks using threads and processes
    demo_cpu_bound()
    demo_io_bound()

    # Key takeaways:
    # - CPU-bound tasks: threads do not help much due to the GIL. Processes do help.
    # - I/O-bound tasks: threads can improve performance significantly, and processes are also an option but may incur more overhead.
    # - asyncio (not shown here) provides concurrency for I/O tasks using a single thread and event loops (cooperative multitasking),
    #   which can also be very efficient for I/O-bound workloads.
