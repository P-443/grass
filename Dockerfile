FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir loguru websockets_proxy
COPY main.py .
CMD ["python", "main.py"]
