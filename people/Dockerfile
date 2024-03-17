FROM python:3.10

WORKDIR /app

COPY ./people/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && apt-get update && apt-get install -y postgresql-client

COPY ./people .

ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=mydatabase
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

# CMD [ "python", "main.py" ]
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]