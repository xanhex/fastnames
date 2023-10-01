FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -U pip &&\
    pip install -r fastnames/requirements.txt --no-cache-dir

CMD ["uvicorn", "fastnames.main:app", "--host", "0.0.0.0", "--port", "8000"]
