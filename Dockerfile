FROM python:3.9-slim
LABEL maintainer="Max Meinhold <mxmeinhold@gmail.com>"

RUN mkdir /opt/minecraft-scan
WORKDIR /opt/minecraft-scan

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY scan.py .

CMD ["python3", "scan.py"]
