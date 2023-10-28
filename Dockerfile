FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./entrypoint.sh ./entrypoint.sh
RUN chmod u+x ./entrypoint.sh

ENTRYPOINT ./entrypoint.sh
