# Используйте легковесный образ Python
FROM python:3.8-slim as builder

# Установите рабочую директорию
WORKDIR /backend

# Установите переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Установите системные зависимости для сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Скопируйте зависимости
COPY requirements.txt .

# Установите зависимости
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Финальный минимальный образ
FROM python:3.8-slim as runner

# Установите рабочую директорию
WORKDIR /backend

# Установите переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Скопируйте зависимости из builder
COPY --from=builder /install /usr/local

# Скопируйте исходный код приложения
COPY . .

# Открыть порт для приложения
EXPOSE 80

# Запуск приложения
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
