FROM python:3.11-slim

WORKDIR /frontend

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# this is the port where container listens
# so if you map Host machine port to this port
# any request coming to the host machine will be passed to this
# port
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
