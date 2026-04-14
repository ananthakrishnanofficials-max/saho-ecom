FROM python:3.10-slim-bullseye

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    python3-yaml \
    && rm -rf /var/lib/apt/lists/*

# Upgrade build tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install
COPY requirements.txt .
RUN pip install --prefer-binary -r requirements.txt \
    && pip install gunicorn

# Copy project
COPY . /app

# Set Django settings
ENV DJANGO_SETTINGS_MODULE=myecom.settings

# Set correct working directory (IMPORTANT)
WORKDIR /app/myecom  # <-- change if needed

# Collect static
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "myecom.wsgi:application", "--bind", "0.0.0.0:8000"]