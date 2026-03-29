FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD https://raw.githubusercontent.com/Gzgod/Grass-Node/main/main.py .
CMD ["python", "main.py"]
