FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]