# GProxy
## Session Based free proxy in Python

## Installation
sudo python setup.py install

## What does GProxy Provides
gproxy.Session() works exactly like requests.Session(), but it also supports proxies.


All functions of requests.Session() will also be availabe in gporxy.Session() 

It will get proxies by itself. Whenever you think that response is slow you can update proxy. For clarification, see the example given below  


## Demo
import gproxy

session = gproxy.Session()

session.get("https://google.com")

If response of the above request is slow, then you can request for a new proxy by calling

session.update_proxy()


