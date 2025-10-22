FROM python:3.11-slim
WORKDIR /app
COPY service/gamma/etl/service_create_table_views_from_sql/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY service/gamma/etl/service_create_table_views_from_sql/app ./app
COPY libraries ./libraries
COPY runtime_definitions ./runtime_definitions
ENV PYTHONPATH=/app/libraries
CMD ["python", "app/main.py"]


