from celery import Celery
import os

BROKER_DEFAULT_USER = os.environ.get("BROKER_DEFAULT_USER")
BROKER_DEFAULT_PASSWORD = os.environ.get("BROKER_DEFAULT_PASSWORD")
BROKER_HOST = os.environ.get("BROKER_HOST")
BROKER_PORT = os.environ.get("BROKER_PORT")
broker_url = f'amqp://{BROKER_DEFAULT_USER}:{BROKER_DEFAULT_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/'

celeryapp = Celery("celery_app", broker=broker_url, backend='rpc://')
celeryapp.conf.imports = [
    'grooming.grooming_worker',
    'rwa.rwa_worker'
]