FROM python:3.12.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

RUN apt update && apt install -y iputils-ping

COPY . .

EXPOSE 7000

CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
