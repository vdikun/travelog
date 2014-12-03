## Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('travelog.photos.tasks', )

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'

def my_on_failure(self, exc, task_id, args, kwargs, einfo):
    print('Oh no! Task failed: {0!r}'.format(exc))

CELERY_ANNOTATIONS = {'*': {'on_failure': my_on_failure}}
