from time import sleep
from faker import Faker

from admin.celery import app
from user.models import UserProfile


@app.task
def hello():
    sleep(.2)
    print('\n' + "Hello from Celery! :D" + '\n')


@app.task
def print_log(x, y):
    print("I'm Celery log...")
    print("I'm starts every minute with Celery Beat in Docker container.")
    print(f"It's just a number - {x ** y}.")


@app.task
def user():
    print("Fillig UserProfile\'s table...")

    UserProfile.objects.create(
        username=Faker().user_name(),
        email=Faker().email(),
        password='9ol8ik7uj',
        role='unknown',
        verifyed_email=False,
    )
