FROM python:3.11-slim
WORKDIR /app
COPY service/airport/etl/service_json_to_client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY service/airport/etl/service_json_to_client/app ./app
COPY libraries/classes ./libraries/classes
COPY libraries/packages ./libraries/packages
COPY libraries/runners ./libraries/runners
COPY libraries/utils ./libraries/utils
COPY runtime_definitions/airport/json_to_client ./runtime_definitions/airport/json_to_client 
ENV PYTHONPATH=/app/libraries
CMD ["python", "app/main.py"]


