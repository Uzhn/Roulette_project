FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY roulette_project/ .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]