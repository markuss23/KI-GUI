FROM python:3.11-slim-bookworm as requirements-stage
WORKDIR /tmp
RUN pip install poetry
RUN pip install poetry-plugin-export
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim-bookworm as build-stage
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get update && apt-get install -y \
    nano \
    curl \
    sqlite3
COPY ./README.md /code/
COPY ./pyproject.toml /code/
COPY ./api /code/api

ENV TZ=Europe/Prague
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# CMD [ "fastapi", "dev", "/code/src/main.py" ]
CMD [ "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000","--reload", "--workers", "4" ]

# gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

# CMD [ "gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]