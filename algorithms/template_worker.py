from celery_app import celeryapp
import time
import random

@celeryapp.task(bind=True)
def template_task(self):
    """Background task that runs a long function with progress reports."""
    total = random.randint(100, 200)
    for i in range(total):
        print({'current': i, 'total': total, 'status': "Fine"})
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': "Fine"})
        
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

@celeryapp.task()
def func1(arg):
    time.sleep(5)
    return arg**2