FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# system deps for psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collect static at build time
RUN python manage.py collectstatic --noinput

# run migrations on startup then serve
CMD bash -lc "python manage.py migrate && gunicorn mysite.wsgi:application --bind 0.0.0.0:8000"
