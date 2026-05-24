FROM python:3.13.3-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ pkg-config python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==2.2.1

WORKDIR /project

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root

COPY app/ ./app/
RUN poetry install --only-root --no-interaction --no-ansi


FROM python:3.13.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /project

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY app/ ./app/
COPY entrypoint.sh /project/entrypoint.sh

RUN chmod +x /project/entrypoint.sh

ENTRYPOINT ["/project/entrypoint.sh"]