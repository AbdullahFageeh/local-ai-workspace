# Python & Systems Engineering Knowledge & Cheatsheet

## Threading & Concurrency Patterns
- **threading.Lock():** Use `with lock:` context managers to guarantee atomic operations in critical sections.
- **threading.RLock():** Reentrant lock allowing the same thread to acquire the lock multiple times without deadlock.
- **Queue.Queue:** Thread-safe FIFO queue for producer-consumer workflows.
- **concurrent.futures.ThreadPoolExecutor:** High-level abstraction for asynchronous thread execution.

## Data Structure Complexities
- **LRU Cache:** O(1) get and put using Hash Map + Doubly Linked List.
- **Trie (Prefix Tree):** O(L) search where L is string length, ideal for autocomplete.
- **Binary Search:** O(log N) search on sorted arrays.
- **Min/Max Heap:** O(1) peek, O(log N) push and pop using `heapq`.

## Clean Code Guidelines
1. Always include explicit type hints (`from typing import Optional, List, Dict, Any`).
2. Write concise docstrings explaining parameters and return values.
3. Handle edge cases (empty collections, None values, index boundaries).
