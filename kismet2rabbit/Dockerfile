FROM python:3

RUN apt-get update && apt-get -y install tcpdump

WORKDIR /usr/src/kismet-stream

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY get_pcap_stream.py .
COPY i80211_detail.py .
COPY pcapng.py .
COPY radiotap.py .
COPY vht.py .

ENTRYPOINT [ "python", "./get_pcap_stream.py" ]
