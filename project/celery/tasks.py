from celery import shared_task


@shared_task
def celery_ping():
    print("Check Celery Connection!")
    return 10


@shared_task(name="task_schedule_work")
def task_schedule_work():
    print("Hello there!")
