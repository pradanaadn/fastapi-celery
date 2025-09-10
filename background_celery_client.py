from multiprocessing import Process
import os
from celery.app import Celery


class Task:
    client: Celery | None = None
    worker: Process | None = None

    @classmethod
    def init_app(cls):
        if not cls.client:
            cls.client = Celery(
                "tasks_queue",
                broker="redis://127.0.0.1:6379",
                backend="redis://127.0.0.1:6379",
            )
            print("Initializing Celery")

    @classmethod
    def get_client(cls) -> Celery:
        if cls.client:
            print("Returning Celery")
            return cls.client
        raise RuntimeError("Celery not initialized")

    @classmethod
    def start_worker(cls):
        cls.client.worker_main(["worker"])

    @classmethod
    def launch_worker(cls):
        cls.worker = Process(target=cls.start_worker, daemon=True)
        cls.worker.start()
        print("Worker started")

    @classmethod
    def stop_worker(cls):
        cls.worker.terminate()
        cls.worker.join()
        print("Worker stopped")
