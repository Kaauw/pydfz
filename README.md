# pyDFZ
Simple tool which download and compile MRT data from RIPE-NCC Website into exabgp format and advertise prefixes to a set of routers.

## Usage 
First of all, you need to configure bgp.yaml present into app/ directory. **Create it if not exists**.

> :warning: Be carefull about latest-bview.gz file size. Compare size between RRC sources and take the smallest one. For example, if you take rrc00, route computation can take severall hours to complete. (Uncompressed file size is almost 8Gb as I wrote theses lines)

```yaml
---
mrts:
  - RIS RAW DATA URL 
  - https://data.ris.ripe.net/rrc26/latest-bview.gz
neighbors:
  - name: <router name>
    mrt: <rrc source name> # Must match rrc source name
    remote_addr: <router address>
    local_addr: <local address>
    local_as: <local AS Number>
    remote_as: <Peer AS Number
    inetnexthop: <IPv4 Next hop>
    inet6nexthop: '<IPv6 Next Hop'
  - name: example
    mrt: rrc26
    remote_addr: 172.17.130.105
    local_addr: 172.17.130.44
    local_as: 65012
    remote_as: 65010
    inetnexthop: 172.17.1.253
    inet6nexthop: '2001:db8:beef::1'
```

### Python virtual environment
```bash
python3 -m venv pydfz-env
source pydfz-env/bin/activate
pip3 install -r requirements.txt
python3 app/create-exa-config.py

env exabgp.api.ack=false exabgp app/conf/exabgp.cfg
```

### Docker
```bash
docker build --tag pydfz .
Sending build context to Docker daemon  38.91kB
Step 1/9 : FROM python:3.9.12-slim-buster
 ---> a52790549fca
Step 2/9 : WORKDIR /app
 ---> Using cache
 ---> 92ba87522701
Step 3/9 : EXPOSE 179
 ---> Using cache
 ---> a84d7351d79c
Step 4/9 : COPY app/ .
 ---> Using cache
 ---> 3df7612da6a0
Step 5/9 : RUN pip3 install -r requirements.txt
 ---> Using cache
 ---> 26bd7959d079
Step 6/9 : RUN python3 create-exa-config.py
 ---> Using cache
 ---> 1105d078a5da
Step 7/9 : RUN chmod 777 conf/*
 ---> Using cache
 ---> b78609ec4b13
Step 8/9 : COPY app/exabgp.env /usr/local/etc/exabgp/exabgp.env
 ---> Using cache
 ---> 1cf369ea31e5
Step 9/9 : ENTRYPOINT [ "exabgp", "conf/exabgp.conf" ]
 ---> Running in 2d9d75741880
Removing intermediate container 2d9d75741880
 ---> e9eea2273c53
Successfully built e9eea2273c53
Successfully tagged pydfz:latest

# Run 
docker run -d --name pydfz --restart always --net=host pydfz                                                                                                                                 
```

## Ressources 
- [RIPE NCC RIS RAW DATA](https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/ris-raw-data)
- [mrtparse](https://github.com/t2mune/mrtparse)
- [exabgp](https://github.com/Exa-Networks/exabgp)
