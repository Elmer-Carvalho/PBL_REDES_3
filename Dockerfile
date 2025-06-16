FROM python:3.9-slim

WORKDIR /app

# Instalar curl para health checks
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app/ /app/app/
COPY contracts/ /app/contracts/

EXPOSE 8000

CMD ["python", "app/main.py"]