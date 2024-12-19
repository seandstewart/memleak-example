FROM python:3.12 as poetry

WORKDIR /app

ENV POETRY_URL="https://install.python-poetry.org"

RUN curl -sSL "${POETRY_URL}" | python3 -

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN /root/.local/bin/poetry export --without-hashes --without-urls --only=main -f requirements.txt -o requirements.txt

FROM python:3.12-slim as dependencies

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1 \
    PIP_NO_INPUT=1

COPY --from=poetry /app/requirements.txt requirements.txt

RUN python -m venv .venv \
    && .venv/bin/pip install -r requirements.txt

FROM python:3.12-slim as main

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ="UTC"

COPY --from=dependencies /app/.venv .venv
COPY schema schema
COPY src src
COPY pyproject.toml pyproject.toml
RUN .venv/bin/pip install -e .

EXPOSE 8080/tcp
ENTRYPOINT [".venv/bin/serve"]
