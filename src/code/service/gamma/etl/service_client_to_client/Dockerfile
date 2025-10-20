FROM python:3.11-slim
WORKDIR /app
COPY service/gamma/etl/service_client_to_client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY service/gamma/etl/service_client_to_client/app ./app
COPY libraries ./libraries
COPY runtime_definitions ./runtime_definitions
ENV PYTHONPATH=/app/libraries
CMD ["python", "app/main.py"]


