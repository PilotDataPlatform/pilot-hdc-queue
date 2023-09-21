FROM python:3.9-buster

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/home/deploy/.local/bin:${PATH}"

WORKDIR /home/deploy

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-root --no-interaction
COPY . .

CMD ["python3", "./main.py"]
