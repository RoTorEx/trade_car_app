# File for building the application image

# Get the Python image
FROM python:3.10-alpine

# Set the working directory of the image
WORKDIR /usr/src/app

# Setting up the environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 and dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Copy pipenv files
COPY Pipfile ./
COPY Pipfile.lock ./

# Set up pipenv and application dependencies
RUN pip install pipenv
RUN set -ex && pipenv install --deploy --system

# Copy and configure the entrypoint.sh script
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy project
COPY . .

# Command to start the project when deployed via Docker
# CMD ["python", "manage.py", "runserver"]

# Run entrypoint.sh script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
