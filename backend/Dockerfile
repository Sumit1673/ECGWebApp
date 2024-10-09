FROM ghcr.io/sumit1673/ml-base:v1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8081
CMD ["fastapi", "run", "src/main.py", "--port", "8081"]