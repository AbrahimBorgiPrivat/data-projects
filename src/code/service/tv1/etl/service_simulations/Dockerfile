FROM python:3.11-slim
WORKDIR /app
COPY service/tv1/etl/service_simulations/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY service/tv1/etl/service_simulations/app ./app
COPY libraries/classes ./libraries/classes
COPY libraries/packages ./libraries/packages
COPY libraries/runners ./libraries/runners
COPY libraries/utils ./libraries/utils
COPY libraries/service_specifik/tv1/simulations ./libraries/service_specifik/tv1/simulations
COPY runtime_definitions/tv1/simulations ./runtime_definitions/tv1/simulations 
ENV PYTHONPATH=/app/libraries
CMD ["python", "app/main.py"]


