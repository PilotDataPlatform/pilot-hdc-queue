FROM docker-registry.ebrains.eu/hdc-services-image/base-image:python-3.10.12-v2 AS socketio-image

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/app/.local/bin:${PATH}"
# RUN chmod +x /home/deploy/gunicorn_starter.sh
COPY ./socketio  ./

RUN poetry install --no-dev --no-root --no-interaction

RUN chown -R app:app /app
USER app

# CMD ["./gunicorn_starter.sh"]
CMD poetry run python run.py
