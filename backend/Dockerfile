# Используйте образ Python как родительский образ
FROM python:3.8-slim as builder

# Установите рабочую директорию в /backend
WORKDIR /backend

# Установите переменные окружения
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# Копируйте только requirements.txt вначале для лучшего использования Docker cache
COPY requirements.txt .

# Установите зависимости
RUN pip install --upgrade pip && \
  pip install -r requirements.txt

# Начинаем новую стадию сборки
FROM python:3.8-slim as runner

WORKDIR /backend
COPY --from=builder /usr/local /usr/local
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
