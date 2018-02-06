import requests
import time
import random
import bs4


class Session(requests.Session):
    '''
    this Session is inherited from `requests.Session` and support proxies
    '''

    def __init__(self, **kwargs):
        '''
        params **kwargs: Optional arguments that ``set_parameters`` takes.
        for more information check documentation of ``set_parameters`` method
        '''
        requests.Session.__init__(self)
        self.set_parameters(**kwargs)
        self.__update_proxy_from_source(True)


    def set_parameters(self, speed_test_url = 'http://www.google.com', speed_test_timeout = 5, country_codes = None, max_num_proxy = 5):
        '''
        all the parameters of this function is very importtant to filter 'good proxies'
        speed_test_url: url where request should be made to check latency
        speed_test_timeout: if for a particular proxy, response doesn't come in this time then proxy is bad, choose this parameter wisely because if its too big you may get bad proxies if its too small then you may miss good proxies.
        country_codes: filter proxies for some specific countries, eg IN, US etc, it can be a string or list or strings
        max_num_proxy: maxinum number of proxies to get
        '''
        self.__speed_test_url = speed_test_url
        self.__speed_test_timeout = speed_test_timeout
        self.__max_num_proxy = max_num_proxy
        if country_codes is not None and not isinstance(country_codes, list):
            country_codes = [country_codes]
        if country_codes:
            country_codes = [country_code.upper() for country_code in country_codes]
        self.__country_codes = country_codes


    def get_parameters(self):
        '''
        get all paramaters like 'speed_test_url', 'speed_test_timeout', 'country_codes', 'country_codes', 'max_num_proxy'
        You can update these paramaters by using 'set_parameters' method
        '''
        return {"speed_test_url": self.__speed_test_url, "speed_test_timeout": self.__speed_test_timeout, "country_codes": self.__country_codes, "max_num_proxy": self.__max_num_proxy}


    def get_num_proxies(self):
        '''
        get total number of proxies in the list
        '''
        return len(self.__all_proxies) - self.__proxy_being_used


    def __time_taken(self, pip):
        try:
            t = time.time()
            res = requests.get(self.__speed_test_url, proxies = pip, timeout = self.__speed_test_timeout)
            if res.status_code != 200:
                return 100
            return time.time()-t
        except Exception as e:
            return 100


    def __get_all_proxies(self):
        page = requests.get('https://free-proxy-list.net/', timeout= 30)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')
        table = soup.find('div', {'class': 'table-responsive'})
        trs = table.find_all('tr')
        proxies_list = []
        for tr in trs[1:-1]:
            tds = tr.find_all('td')
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            if tds[6].text.strip()=='yes' and tds[4].text.strip() != "transparent" and (self.__country_codes is None or tds[2].text.strip() in self.__country_codes):
                proxies_list.append({"https": ip+ ':'+ port, "http": ip+ ':'+ port})
        return proxies_list


    def __filter_good_proxies(self, proxies):
        good_proxies = []
        for proxy in proxies:
            time_taken1 = self.__time_taken(proxy)
            if time_taken1 < 100:
                good_proxies.append((time_taken1, proxy))
                if len(good_proxies) == self.__max_num_proxy:
                    return sorted(good_proxies)
        return sorted(good_proxies)


    def __get_proxy(self, **kwargs):
        ips = self.__get_all_proxies()
        ips = self.__filter_good_proxies(ips)
        return [ip[1] for ip in ips]


    def __update_proxy_from_source(self, from_init = False):
        if from_init:
            print("getting proxies")
        else:
            print("refreshing proxy list")
        self.__all_proxies = self.__get_proxy()
        if not len(self.__all_proxies):
            raise Exception("no proxies found for your search, try using different country codes or increasing timeout")
        self.last_refreshed = time.time()
        self.__proxy_being_used = 1
        self.proxies = self.__all_proxies[0]


    def update_proxy(self):
        '''
        if current proxy is slow, you can update proxy by calling this method.
        '''
        if (self.__proxy_being_used < len(self.__all_proxies)) and (time.time() - self.last_refreshed < 600):
            print("getting proxy from cache")
            self.proxies = self.__all_proxies[self.__proxy_being_used]
            self.__proxy_being_used += 1
        else:
            self.__update_proxy_from_source()
        print("new proxy: %r"%self.proxies)


    def get(self, *args, **kwargs):

        for i in range(3):
            try:
                res = super(Session, self).get(*args, **kwargs)
                if res.status_code not in (407,503):
                    return res
                else:
                    self.update_proxy()
            except (requests.exceptions.ProxyError,requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout) as e:
                #print("%r : %r"%(type(e), e))
                self.update_proxy()

        return super(Session, self).get(*args, **kwargs)


    def post(self, *args, **kwargs):

        for i in range(3):
            try:
                res = super(Session, self).post(*args, **kwargs)
                if res.status_code not in (407,503):
                    return res
                else:
                    self.update_proxy()
            except (requests.exceptions.ProxyError,requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout) as e:
                #print("%r : %r"%(type(e), e))
                self.update_proxy()

        return super(Session, self).post(*args, **kwargs)
