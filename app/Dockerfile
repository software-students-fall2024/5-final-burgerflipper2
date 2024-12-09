FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . /app

EXPOSE 3000

ENV FLASK_ENV=production

CMD ["python", "app.py", "login.py"]