# invitro/shop/tasks.py
from celery import shared_task
from invitro.celery import app

@app.task
def hello():
	print('hurllo!')



@shared_task
def adding_task(x, y):  
    return x + y