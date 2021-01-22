import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('product')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'insert_into_bd':{
        'task': 'product.tasks.create_product',
        'schedule' : 30
    },
    'insert_into_bq': {
       'task': 'product.tasks.import_to_bq',
        'schedule': 60
   },
  #  'check_similarity':{
  #     'task': 'product.tasks.check_on_dublicates',
  #      'schedule': 5
  #  }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')