FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app
COPY server.py .

RUN pip install flask playwright
RUN playwright install --with-deps chromium

CMD ["python", "server.py"]
