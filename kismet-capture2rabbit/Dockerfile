FROM python:3-alpine

WORKDIR /usr/src/kiscap2rabbit

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY i80211_detail.py .
COPY pcapng.py .
COPY radiotap.py .
COPY vht.py .
COPY kismet2rabbit.py .

ENTRYPOINT [ "python", "./kismet2rabbit.py" ]
