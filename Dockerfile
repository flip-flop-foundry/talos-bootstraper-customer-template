FROM python:3.12-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

ENV APP_NAME=PLACEHOLDER_APP
ENV APP_VERSION=dev

EXPOSE 8080

CMD ["python", "app.py"]
