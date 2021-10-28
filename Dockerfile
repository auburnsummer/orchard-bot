FROM python:3.8

RUN apt-get update && apt-get -y install sqlite3 libsqlite3-dev

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "main:app"]
