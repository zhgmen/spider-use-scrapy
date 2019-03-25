import requests
import json
from datetime import datetime,timedelta
from urllib3.exceptions import ConnectTimeoutError
class MyException(Exception):
    def __init__(self, message):
        super(MyException, self).__init__()
        self.message = message

class IPProxy(object):

    def __init__(self):
        self.expired_time = None
        self.current_proxy = None
        self._parse_proxy()
    def _parse_proxy(self):
        proxy_model = self._get_proxy()
        if not proxy_model:
            raise MyException('获取代理地址失败！')
        model_time = proxy_model['expire_time']
        data, time = model_time.split(" ")
        year, month, day = data.split('-')
        hour, minute, second = time.split(':')
        self.expired_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute),
                                     second=int(second))
        self.current_proxy = "https://{}:{}".format(proxy_model['ip'], proxy_model['port'])

    @property
    def proxy(self):
        while True:
            if not self._test_proxy():
                self._parse_proxy()
            return self.current_proxy

    def _test_proxy(self):
        # 测试代理是否可用
        url = 'https://www.baidu.com'
        try:
            proxies = {"https": self.current_proxy}
            requests.get(url=url,proxies=proxies, timeout=3)
        except ConnectTimeoutError as e:
            return False
        return True

    @property
    def is_expired(self):
        if self.expired_time-datetime.now() < timedelta(seconds=3):
            return True
        return False



    def _get_proxy(self):
        proxy_api = ""
        result = requests.get(url=proxy_api).text
        json_str = json.load(result)
        return json_str['data'][0]

