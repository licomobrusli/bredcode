FROM python:3.8

CMD ["python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "manage.py", "runserver", "0.0.0.0:8000"]

# set container timezone to madrid
ENV TZ=Europe/Madrid

# Copy wait-for-it
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# setting work directory
WORKDIR /usr/src/app

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install psycopg tendencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip pipenv flake8
COPY Pipfile* ./
RUN pipenv install --system --ignore-pipfile

COPY . .

# lint
RUN flake8 --ignore=E501,F401 .
