from __future__ import annotations

import threading
import time

from .errors import A2APIError


class Budget:
    def __init__(self, deadline_ms: int, max_calls: int):
        self.deadline = time.monotonic() + deadline_ms / 1000
        self.max_calls = max_calls
        self.calls = 0
        self.cancelled = threading.Event()
        self.lock = threading.Lock()

    def remaining(self) -> float:
        remaining = self.deadline - time.monotonic()
        if self.cancelled.is_set():
            raise A2APIError("EXECUTION_STOPPED", "Execution stopped after a required step failed.", status=502)
        if remaining <= 0:
            raise A2APIError("DEADLINE_EXCEEDED", "Execution deadline was exceeded.", status=504)
        return remaining

    def claim(self) -> None:
        with self.lock:
            self.remaining()
            if self.calls >= self.max_calls:
                raise A2APIError("CALL_BUDGET_EXCEEDED", "Backend call budget was exceeded.", status=502)
            self.calls += 1
