FROM python:3.9.12-slim-buster

WORKDIR /app

# Expose BGP PORT 179
EXPOSE 179

COPY app/ .
RUN pip3 install -r requirements.txt

# Create configuration
RUN python3 create-exa-config.py
RUN chmod 777 conf/*

# COPY Exabgp.env to /usr/local/etc/exabgp/exabgp.env
COPY app/exabgp.env /usr/local/etc/exabgp/exabgp.env

# Run Exabgp
ENTRYPOINT [ "exabgp",  "conf/exabgp.conf" ]
