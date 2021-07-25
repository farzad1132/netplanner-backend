"""
    This modules contains background task manager configs
"""

import os

from celery import Celery

BROKER_DEFAULT_USER = os.environ.get("BROKER_DEFAULT_USER")
BROKER_DEFAULT_PASSWORD = os.environ.get("BROKER_DEFAULT_PASSWORD")
BROKER_HOST = os.environ.get("BROKER_HOST")
BROKER_PORT = os.environ.get("BROKER_PORT")
BACKEND_HOST = os.environ.get("BACKEND_HOST")
broker_url = f'amqp://{BROKER_DEFAULT_USER}:{BROKER_DEFAULT_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/'
backend_url = f"redis://{BACKEND_HOST}:6379/0"

celeryapp = Celery("celery_app", broker=broker_url, backend=backend_url)
celeryapp.conf.imports = [
    'grooming.grooming_worker',
    'rwa.rwa_worker'
]
celeryapp.conf.task_track_started = True
