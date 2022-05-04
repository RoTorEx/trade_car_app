from time import sleep

from admin.celery import app


@app.task
def hello():
    sleep(.2)
    print('\n' + "Hello from Celery! :D" + '\n')
