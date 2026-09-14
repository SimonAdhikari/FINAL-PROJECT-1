"""
Multithreaded Logger Module.

Implements Part E requirement: Multithreading for activity logging.
Uses a Producer-Consumer pattern with queue.Queue and threading.Thread
to write audit trails asynchronously to disk without blocking user workflows.
"""

import os
import time
import queue
import threading
from datetime import datetime

class MultithreadedLogger:
    """Thread-safe background logger for system user activities."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, log_file_path: str = "data/activity_logs.txt"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_logger(log_file_path)
            return cls._instance

    def _init_logger(self, log_file_path: str):
        self.log_file_path = log_file_path
        os.makedirs(os.path.dirname(os.path.abspath(self.log_file_path)), exist_ok=True)
        self.log_queue = queue.Queue()
        self.is_running = True

        # Start worker thread
        self.worker_thread = threading.Thread(
            target=self._process_logs,
            name="SecurityLoggerThread",
            daemon=True
        )
        self.worker_thread.start()

    def _process_logs(self):
        """Worker loop reading log entries from queue and writing to disk."""
        while self.is_running or not self.log_queue.empty():
            try:
                entry = self.log_queue.get(timeout=0.5)
                if entry is None:  # Shutdown signal
                    break

                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write(entry + "\n")

                self.log_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[Logger Error] Failed to write log: {e}")

    def log(self, user_id: str, action: str, status: str = "SUCCESS", details: str = ""):
        """Enqueues a log entry asynchronously."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thread_name = threading.current_thread().name
        formatted_entry = f"[{timestamp}] [Thread: {thread_name}] [User: {user_id}] [Action: {action}] [Status: {status}] - {details}"
        self.log_queue.put(formatted_entry)

    def shutdown(self):
        """Cleanly shuts down worker thread after processing pending queue."""
        if not self.is_running:
            return
        self.is_running = False
        self.log_queue.put(None)
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)

    def get_logs(self) -> list[str]:
        """Reads and returns all logged activities from file."""
        if not os.path.exists(self.log_file_path):
            return []
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except Exception:
            return []
