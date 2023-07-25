FROM arm32v7/python:3.10-slim
WORKDIR /app
RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]