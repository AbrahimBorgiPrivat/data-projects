FROM python:3.11-slim
WORKDIR /app
COPY service/gamma/etl/service_client_to_csv/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY service/gamma/etl/service_client_to_csv/app ./app
COPY libraries/classes ./libraries/classes
COPY libraries/packages ./libraries/packages
COPY libraries/runners ./libraries/runners
COPY libraries/utils ./libraries/utils
COPY runtime_definitions/gamma/client_to_csv ./runtime_definitions/gamma/client_to_csv
ENV PYTHONPATH=/app/libraries
CMD ["python", "app/main.py"]


