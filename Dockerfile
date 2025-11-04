# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system deps for many Python packages (adjust as needed)
RUN apt-get update && apt-get install -y build-essential libpq-dev netcat && rm -rf /var/lib/apt/lists/*

# install pipenv/poetry or requirements.txt approach
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# collect static files (use env var to control)
ARG DJANGO_ENV=production
ENV DJANGO_ENV=${DJANGO_ENV}
RUN python manage.py collectstatic --noinput

# run migrations at container start (entrypoint handles it)
COPY ./compose/production/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]
