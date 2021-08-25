from celery import shared_task
from fastapi import Request


@shared_task(name="check_connection")
def celery_ping():
    print("Check Celery Connection!")
    return 10
