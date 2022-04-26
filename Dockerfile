# File for building the application image

# Get the Python image
FROM python:3.10-alpine

# Set the working directory of the image
WORKDIR /trade_car_app

# Setting up the environment
ENV PYTHONUNBUFFERED 1

# Install psycopg2 and dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Copy files
COPY . /trade_car_app

# Set up pipenv and application dependencies
RUN pip3 install pipenv
# RUN pipenv install --ignore-pipfile --system
RUN pipenv install --deploy --system
