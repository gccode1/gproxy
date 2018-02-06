# GProxy
## About GProxy
gproxy is a robust http(s), free and fast proxy service build for the sole purpose of web crawling. It is build on top of requests.Session and hence provides all requests functionalities. gproxy gets all proxies from https://free-proxy-list.net and identifies the best proxy(ies) for your specific task. It automatically detects network latency and updates proxies to provide optimal speed.

## Installation
```
git clone https://github.com/gccode1/gproxy
cd gproxy
```
For Default version of Python
```
sudo python setup.py install
```
For a specific python version, ex python3
```
sudo python3 setup.py install
```

## Usage
```
import gproxy

session = gproxy.Session()

session.get("https://google.com")
```

### Update proxy manually
```
session.update_proxy()
```
