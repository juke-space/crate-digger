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


class BurstHttpAdapter(requests.adapters.HTTPAdapter):
    throttle = None
    max_hits = None
    hits = None
    burst_window = None
    total_window = None
    timestamp = None

    def __init__(self, pool_connections=requests.adapters.DEFAULT_POOLSIZE,
                 pool_maxsize=requests.adapters.DEFAULT_POOLSIZE, max_retries=requests.adapters.DEFAULT_RETRIES,
                 pool_block=requests.adapters.DEFAULT_POOLBLOCK, burst_window=DEFAULT_BURST_WINDOW,
                 wait_window=DEFAULT_WAIT_WINDOW):
        self.max_hits = pool_maxsize
        self.hits = 0
        self.burst_window = burst_window
        self.wait_window = wait_window
        self.now = None
        self.burst_start = None
        super(BurstHttpAdapter, self).__init__(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                            max_retries=max_retries, pool_block=pool_block)

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        response = None
        wait_time = self.throttle()
        if wait_time > datetime.timedelta(0):
            gevent.sleep(wait_time.total_seconds(), ref=True)

        response = super(BurstHttpAdapter, self).send(request, stream=stream, timeout=timeout,
                                                       verify=verify, cert=cert, proxies=proxies)
        result = json.loads(response.content.decode())
        if "error" in result and result["error"] == 29:
            gevent.sleep(self.wait_time.total_seconds(), ref=True)
        return response

    def throttle(self):
        self.now = datetime.datetime.utcnow()
        if not self.burst_start:
            self.burst_start = datetime.datetime.utcnow()

        if self.now < self.burst_start + self.burst_window and self.hits < self.max_hits:
            self.hits += 1
            return datetime.timedelta(0)

        self.burst_start = None
        return self.wait_window

def send_async_requests(
    urls: List[str],
    max_concurrent_requests: int,
    burst_window: datetime.timedelta = datetime.timedelta(seconds=15),
    wait_window: datetime.timedelta = datetime.timedelta(seconds=10),
):
    requests_adapter = BurstHttpAdapter(
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
