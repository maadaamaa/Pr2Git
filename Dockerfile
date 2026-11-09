
FROM python:3.11.10-slim

WORKDIR /app

COPY schedule.py .
COPY schedule.json.example .

ENV APP_PORT=8110

CMD ["python", "schedule.py"]
