FROM python:3-alpine

RUN apk add --no-cache tcpdump

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pcapng.py .
COPY parser .
COPY kismet2rabbit.py .

ENTRYPOINT [ "python", "./kismet2rabbit.py" ]
