FROM python:3.13.3-alpine3.21

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["sh", "-c", "python app/init_dummy_routes.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
