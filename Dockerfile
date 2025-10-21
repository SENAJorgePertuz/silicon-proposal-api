# Imagen base con Python
FROM python:3.11-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar LibreOffice y dependencias necesarias
RUN apt-get update && apt-get install -y libreoffice && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la app
COPY app ./app
COPY Procfile ./Procfile
COPY runtime.txt ./runtime.txt

# Exponer el puerto (Render usa 10000)
EXPOSE 10000

# Comando para ejecutar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
