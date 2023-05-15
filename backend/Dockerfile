FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .
ENV PYTHONPATH /app/api_foodgram
CMD ["gunicorn", "api_foodgram.wsgi:application", "--bind", "0:8000" ]