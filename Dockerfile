FROM python:3.12-slim AS builder

# System setup
RUN apt update -y && apt install -y libjpeg-dev

WORKDIR /usr/src/app

# Copy source
COPY requirements.txt requirements.txt

## Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencies
RUN pip install --user -r requirements.txt --no-cache-dir

FROM python:3.12-slim

# Dependencies
RUN apt update -y && apt install -y supervisor curl

WORKDIR /usr/src/app

COPY . .
COPY --from=builder /root/.local /root/.local

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

# Configuration
COPY conf/supervisor.conf /etc/supervisord.conf
# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/v1/status || exit 1

# Execution
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
