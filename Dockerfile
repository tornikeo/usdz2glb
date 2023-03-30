FROM python:3.10
# Fix tzdata asking for "Please select the geographic area in which you live..."
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get install git curl -y

# To fix pyzmq build error "g++ not found"
RUN apt install build-essential -y
WORKDIR /workdir
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENV PORT 8080

ARG DEVELOPMENT='False'
ENV DEVELOPMENT ${DEVELOPMENT}

ARG GCLOUD_BUCKET='vimage-image-api-io-tmp24h'
ENV GCLOUD_BUCKET ${GCLOUD_BUCKET}

ARG BACKEND_URL
ENV BACKEND_URL ${BACKEND_URL}

EXPOSE $PORT
# DEVELOPMENT=False uvicorn main:app --host 0.0.0.0 --port 8090 --reload --log-level debug
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT} --log-level debug 