FROM python:3-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY kismetalert2rabbit.py .

ENTRYPOINT [ "python", "./kismetalert2rabbit.py" ]
