# Base image com Python
FROM python:3.10

# Instala o htop#
RUN apt-get update && apt-get install -y htop && apt-get clean

# Configura o diretório de trabalho
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .
COPY worker/ .

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do worker para o contêiner
COPY worker_main.py .

RUN pip install ./dist/worker-0.1.0-py3-none-any.whl --force-reinstall

# Comando padrão para executar o worker
CMD ["python", "worker_main.py"]