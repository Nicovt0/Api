FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y \
        pkg-config \
        default-libmysqlclient-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requerimientos.txt .
RUN pip install --upgrade pip && pip install -r requerimientos.txt
COPY . .
RUN cd /app
EXPOSE 8000
CMD [ "python","manage.py","runserver", "0.0.0.0:8000" ]