FROM python:3.10

WORKDIR /app

COPY ./kick/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./kick .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7222" ]