FROM python:3-alpine

RUN pip install --no-cache-dir pika

COPY printESSIDs.py .

CMD ["python","printESSIDs.py"]
