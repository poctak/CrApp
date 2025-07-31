# Použij oficiální Python 3.11 image jako základ
FROM python:3.11-slim

# Nastav pracovní adresář v kontejneru
WORKDIR /app

# Zkopíruj requirements (pokud máš) a GainPrices.py do kontejneru
COPY GainPrices.py .

# Instaluj závislosti (tady jen requests)
RUN pip install --no-cache-dir requests

# Spuštění skriptu při startu kontejneru
CMD ["python", "GainPrices.py"]
