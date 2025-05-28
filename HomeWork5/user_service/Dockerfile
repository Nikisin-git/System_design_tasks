FROM python:3.13.3-alpine3.21
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY ./alembic ./alembic
COPY ./app ./app

CMD ["sh", "-c", "alembic upgrade head && python app/init_admin.py && python app/init_dummy_users.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]