# Oficiální Python image
FROM python:3.11-slim

WORKDIR /app

# Kopíruj jen skript
COPY GainPrices.py .

# Nainstaluj jen to, co skutečně používáš
RUN pip install --no-cache-dir websockets

# Spusť aplikaci
CMD ["python", "GainPrices.py"]
