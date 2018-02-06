# GProxy
## Session Based free proxy in Python

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

## What does GProxy Provides
gproxy is build on top of requests.Session and supports proxies as well.
It gets all proxies from https://free-proxy-list.net/ and use them one by one, whenever there there is a latency in response, it automatically updates proxy. You can also force it to update proxy.


## Demo


### Normal Use
```
import gproxy

session = gproxy.Session()

session.get("https://google.com")
```

### Update proxy manually
```
session.update_proxy()
```
