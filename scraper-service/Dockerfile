FROM python:latest

LABEL maintainer="Vlad Kudelko <vlad1kudelko@gmail.com>"

WORKDIR /home/scraper-service

COPY scraper-service/pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

COPY common_schemas /home/common_schemas

RUN poetry install --no-interaction --no-ansi

COPY scraper-service/app app
COPY scraper-service/.env .

ENTRYPOINT ["python", "-u", "app/main.py"]
