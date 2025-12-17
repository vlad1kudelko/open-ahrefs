FROM python:latest

LABEL maintainer="Vlad Kudelko <vlad1kudelko@gmail.com>"

WORKDIR /home/admin-service

COPY admin-service/pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

COPY common_schemas /home/common_schemas

RUN poetry install --no-interaction --no-ansi

COPY admin-service/app app
COPY admin-service/.env .

ENTRYPOINT ["python", "-u", "app/main.py"]
