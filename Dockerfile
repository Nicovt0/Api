FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
        pkg-config \
        default-libmysqlclient-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requerimientos.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requerimientos.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]