# GProxy
## Session Based free proxy in Python

## Installation
```
git clone https://github.com/gccode1/gproxy
cd gproxy
sudo python setup.py install
```

## What does GProxy Provides
gproxy is build on top of requests.Session and supports proxies as well.
It gets all proxies from https://free-proxy-list.net/ and use them one by one, whenever there there is a latency in response, it automatically update proxy. You can also force it to update proxy.


## Demo

```
import gproxy

session = gproxy.Session()

session.get("https://google.com")

session.update_proxy() # In case response of above request was slow
```
