FROM python:3.9-slim

WORKDIR /app

COPY . /app

EXPOSE 12345

CMD ["python", "gps/ws.py"]
