import os
from datetime import datetime
from background_celery_client import Task as BackgroundCeleryTask

BackgroundCeleryTask.init_app()
app = BackgroundCeleryTask.get_client()


@app.task
def dummy_task():
    folder = "/tmp/celery"
    os.makedirs(folder, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%s")
    with open(f"{folder}/task-{now}.txt", "w") as f:
        f.write("hello!")
