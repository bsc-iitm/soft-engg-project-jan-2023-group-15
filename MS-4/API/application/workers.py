from celery import Celery
from flask import current_app as app


celery = Celery("Application Jobs")
celery.conf.update(timezone='Asia/Kolkata')
# Create a subclass of task that wraps the task execution in 
# an application context. So its available
class ContextTask(celery.Task):
    def __call__(self, *args, **kwds):
        with app.app_context():
            return self.run(*args, **kwds)