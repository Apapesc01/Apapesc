# Dockerfile

FROM python:3.12-slim

# Atualiza pacotes do sistema para corrigir vulnerabilidades
RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN apt-get update && apt-get install -y git && apt-get clean

# Define workdir
WORKDIR /code

# Copia os requirements
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o projeto
COPY . /code/

# Variável para não criar .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Exemplo: prepara para usar o .env
RUN pip install python-dotenv

# Porta padrão (ajuste se necessário)
EXPOSE 8000

# Comando de start padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


#CMD ["gunicorn", "zzApp_core.wsgi:application", "--bind", "0.0.0.0:8000"]
