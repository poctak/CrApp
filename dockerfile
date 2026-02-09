# Použij oficiální Python 3.11 slim
FROM python:3.11-slim

# Nastav pracovní adresář
WORKDIR /app

# Zkopíruj requirements a nainstaluj knihovny
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj skript do kontejneru
COPY GainPrices.py .

# Spusť aplikaci při startu kontejneru
CMD ["python", "GainPrices.py"]
