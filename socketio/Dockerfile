FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get install -y vim-tiny less && \
    ln -s /usr/bin/vim.tiny /usr/bin/vim && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd --gid 1004 deploy && \
    useradd --home-dir /home/deploy \
    --create-home \
    --uid 1004 \
    --gid 1004 \
    --shell /bin/sh \
    --skel /dev/null deploy

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /home/deploy

RUN chown -R deploy:deploy /home/deploy
ENV PATH="/home/deploy/.local/bin:${PATH}"
# RUN chmod +x /home/deploy/gunicorn_starter.sh
COPY .  ./
RUN poetry install --no-dev --no-root --no-interaction

USER deploy
# CMD ["./gunicorn_starter.sh"]
CMD poetry run python run.py
