FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app
COPY server.py .

RUN pip install flask

CMD ["python", "server.py"]
