# freelance/celery.py
from celery import Celery

app = Celery('freelance')

app.config_from_object('celeryconfig')

app.autodiscover_tasks(['website'])


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
