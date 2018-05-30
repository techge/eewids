FROM python:3-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY rogueap.py .

RUN mkdir lists

CMD ["python","rogueap.py","--train"]
