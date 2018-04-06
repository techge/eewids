FROM python:3-alpine

RUN pip install --no-cache-dir pika

COPY alert-print.py .

CMD ["python","alert-print.py"]
