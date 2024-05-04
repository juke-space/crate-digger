FROM python:3.11-slim-buster

WORKDIR /home

RUN pip install pdm==2.15.1

COPY ./pyproject.toml ./
COPY ./pdm.lock ./
COPY ./tests/__init__.py ./tests/test_lastfm_requests.py ./tests/
COPY ./.env ./tests
COPY ./crate_digger ./crate_digger

RUN pdm sync --prod --no-editable
RUN pdm run pytest

CMD ["pdm", "run", "app"]
