FROM docker-registry.ebrains.eu/hdc-services-image/base-image:python-3.10.12-v2 AS consumer-image

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/app/.local/bin:${PATH}"

COPY ./consumer/poetry.lock ./consumer/pyproject.toml ./
RUN poetry install --no-dev --no-root --no-interaction
COPY ./consumer .

RUN chown -R app:app /app
USER app

CMD ["python3", "./main.py"]
