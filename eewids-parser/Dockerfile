FROM python:3-alpine

RUN apk add --no-cache tcpdump

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY parser .
COPY eewids-parser.py .

ENTRYPOINT [ "python", "./eewids-parser.py" ]
