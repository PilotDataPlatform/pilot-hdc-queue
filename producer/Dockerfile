FROM docker-registry.ebrains.eu/hdc-services-image/base-image:python-3.10.12-v2 AS production-environment

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY ./producer/poetry.lock ./producer/pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction

FROM production-environment AS producer-image

COPY ./producer  ./

RUN chown -R app:app /app
USER app

CMD ["python3", "-m", "producer"]
