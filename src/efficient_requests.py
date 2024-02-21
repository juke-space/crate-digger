import json
import grequests
import requests
import gevent
import datetime
from typing import List, Union

DEFAULT_BURST_WINDOW = datetime.timedelta(seconds=5)
DEFAULT_WAIT_WINDOW = datetime.timedelta(seconds=15)


def make_request(request_url: str) -> Union[None, dict]:
    result = requests.get(request_url)
    if result.status_code == 200:
        return json.loads(result.content.decode())
    elif result.status_code == 404:
        raise Exception(f"No result returned for {request_url}. Request invalid.")


class BurstThrottle(object):
    max_hits = None
    hits = None
    burst_window = None
    total_window = None
    timestamp = None

    def __init__(self, max_hits, burst_window, wait_window):
        self.max_hits = max_hits
        self.hits = 0
        self.burst_window = burst_window
        self.total_window = burst_window + wait_window
        self.timestamp = datetime.datetime.min

    def throttle(self):
        now = datetime.datetime.utcnow()
        if now < self.timestamp + self.total_window:
            if (now < self.timestamp + self.burst_window) and (self.hits < self.max_hits):
                self.hits += 1
                return datetime.timedelta(0)
            else:
                return self.timestamp + self.total_window - now
        else:
            self.timestamp = now
            self.hits = 1
            return datetime.timedelta(0)

class MyHttpAdapter(requests.adapters.HTTPAdapter):
    throttle = None

    def __init__(self, pool_connections=requests.adapters.DEFAULT_POOLSIZE,
                 pool_maxsize=requests.adapters.DEFAULT_POOLSIZE, max_retries=requests.adapters.DEFAULT_RETRIES,
                 pool_block=requests.adapters.DEFAULT_POOLBLOCK, burst_window=DEFAULT_BURST_WINDOW,
                 wait_window=DEFAULT_WAIT_WINDOW):
        self.throttle = BurstThrottle(pool_maxsize, burst_window, wait_window)
        super(MyHttpAdapter, self).__init__(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                            max_retries=max_retries, pool_block=pool_block)

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        response = None
        wait_time = self.throttle.throttle()
        if wait_time > datetime.timedelta(0):
            gevent.sleep(wait_time.total_seconds(), ref=True) # NOTE: this is waiting an insane amount of time. Figure out why.
            wait_time = self.throttle.throttle()

        response = super(MyHttpAdapter, self).send(request, stream=stream, timeout=timeout,
                                                       verify=verify, cert=cert, proxies=proxies)
        return response


def send_async_requests(
    urls: List[str],
    max_concurrent_requests: int,
    burst_window: datetime.timedelta = datetime.timedelta(seconds=0),
    wait_window: datetime.timedelta = datetime.timedelta(seconds=0),
):
    requests_adapter = MyHttpAdapter(
        pool_connections=max_concurrent_requests,
        pool_maxsize=max_concurrent_requests,
        max_retries=0,
        pool_block=False,
        burst_window=burst_window,
        wait_window=wait_window,
    )

    requests_session = requests.session()
    requests_session.mount("http://", requests_adapter)
    requests_session.mount("https://", requests_adapter)

    unsent_requests = (
        grequests.get(
            url,
            #  hooks={'response': handle_response},
            session=requests_session,
        )
        for url in urls
    )
    return grequests.map(unsent_requests, size=max_concurrent_requests)
