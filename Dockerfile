FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml README.md ./
COPY app ./app

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY run.py ./

ENV FLASK_APP=run.py
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
