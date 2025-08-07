FROM python:3.11-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install --upgrade pip && pip install -r requirement.txt

COPY . .

ENV FLASK_APP = app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]