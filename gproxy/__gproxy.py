import requests
import time
from copy import deepcopy
import random
import bs4


class Session(requests.Session):

    def __init__(self):
        requests.Session.__init__(self)
        self.__update_proxy_from_source()


    def __time_taken(self, pip1, timeout = 1):
        pip = deepcopy(pip1)
        pip.pop("http")
        try:
            t = time.time()
            requests.get('http://www.google.com', proxies = pip, timeout = timeout)
            return time.time()-t
        except Exception as e:
            return 100


    def __get_all_proxies(self):
        page = requests.get('https://free-proxy-list.net/', timeout= 30)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        table = soup.find('div', {'class': 'table-responsive'})
        trs = table.find_all('tr')
        proxies_list = []
        for tr in xrange(1, len(trs)-1):
            tds = trs[tr].find_all('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            if tds[6].text.strip()=='yes' and tds[4].text.strip() == "anonymous":
                proxies_list.append({"https": ip+ ':'+ port, "http": ip+ ':'+ port})
        return proxies_list


    def __filter_good_proxies(self, proxies, **kwargs):
        good_proxies = []
        for proxy in proxies:
            time_taken1 = self.__time_taken(proxy, **kwargs)
            if time_taken1 < 100:
                good_proxies.append((time_taken1, proxy))
        return sorted(good_proxies)


    def __get_proxy(self, **kwargs):
        ips = self.__get_all_proxies()
        ips = self.__filter_good_proxies(ips)
        return [ip[1] for ip in ips]


    def __update_proxy_from_source(self):
        print "refreshing proxy list"
        self.all_proxies = self.__get_proxy()
        self.last_refreshed = time.time()
        self.proxy_being_used = 1
        self.proxies = self.all_proxies[0]

    def update_proxy(self):
        if (self.proxy_being_used < len(self.all_proxies)) and (time.time() - self.last_refreshed < 600):
            print "returning proxy from cache"
            self.proxies = self.all_proxies[self.proxy_being_used]
            self.proxy_being_used += 1
        else:
            self.__update_proxy_from_source()
        print "new proxy: ", self.proxies


    def get(self, *args, **kwargs):

        for i in range(3):
            try:
                return super(PSession, self).get(*args, **kwargs)
            except (requests.exceptions.ProxyError,requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout) as e:
                #print type(e), ":", e
                self.update_proxy()

        return super(PSession, self).get(*args, **kwargs)



    def post(self, *args, **kwargs):

        for i in range(3):
            try:
                return super(PSession, self).post(*args, **kwargs)
            except (requests.exceptions.ProxyError,requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout) as e:
                #print type(e), ":", e
                self.update_proxy()

        return super(PSession, self).post(*args, **kwargs)
