FROM python:3.10-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY uwsgi/uwsgi.ini .
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /opt/app/entrypoint.sh && chmod +x /opt/app/entrypoint.sh

RUN mkdir -p /var/www/static /var/www/media \
    && addgroup --system app \
    && adduser --system --ingroup app --no-create-home app \
    && chown -R app:app /opt/app /var/www

COPY --chown=app:app . .
RUN chmod +x /opt/app/entrypoint.sh

USER root
EXPOSE 8000
ENTRYPOINT ["/opt/app/entrypoint.sh"]
