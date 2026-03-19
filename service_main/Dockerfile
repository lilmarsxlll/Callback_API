FROM python:3.14.3-slim

WORKDIR /app
RUN pip install --upgrade pip wheel "poetry==2.2.1"
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY ./service_main .
CMD ["python", "main.py"]