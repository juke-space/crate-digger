import datetime
import json
import traceback
from typing import List, Union

import grequests
import requests
import gevent


def make_request(request_url: str) -> Union[None, dict]:
    result = requests.get(request_url)
    if result.status_code == 200:
        return json.loads(result.content.decode())
    elif result.status_code == 404:
        raise Exception(f"No result returned for {request_url}. Request invalid.")


def send_async_requests(
    urls: List[str],
    max_concurrent_requests: int,
    burst_window: datetime.timedelta = datetime.timedelta(seconds=10),
    wait_window: datetime.timedelta = datetime.timedelta(seconds=30),
):
    requests_adapter = BurstHttpAdapter(
        burst_window,
        wait_window,
        pool_connections=max_concurrent_requests,
        pool_maxsize=max_concurrent_requests,
        max_retries=0,
        pool_block=False
    )

    requests_session = requests.session()
    requests_session.mount("http://", requests_adapter)

    unsent_requests = (
        grequests.get(
            url,
            session=requests_session,
        )
        for url in urls
    )

    return grequests.map(unsent_requests, size=max_concurrent_requests)


class BurstHttpAdapter(requests.adapters.HTTPAdapter):
    burst_window = None
    total_window = None
    timestamp = None

    def __init__(
        self, burst_window, wait_window=datetime.timedelta(seconds=15),
        pool_connections=requests.adapters.DEFAULT_POOLSIZE,
        pool_maxsize=requests.adapters.DEFAULT_POOLSIZE,
        max_retries=requests.adapters.DEFAULT_RETRIES,
        pool_block=requests.adapters.DEFAULT_POOLBLOCK
    ):
        self.burst_window = burst_window
        self.wait_window = wait_window
        self.now = None
        self.burst_start = None
        super(BurstHttpAdapter, self).__init__(
            pool_connections=pool_connections, pool_maxsize=pool_maxsize,
            max_retries=max_retries, pool_block=pool_block)

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None,
        proxies=None
    ):
        response = None
        wait_time = self._throttle()
        if wait_time > datetime.timedelta(0):
            gevent.sleep(wait_time.total_seconds(), ref=True)

        try:
            response = super(BurstHttpAdapter, self).send(
                request, stream=stream, timeout=timeout, verify=verify,
                cert=cert, proxies=proxies)
            result = json.loads(response.content.decode())
            if "error" in result and result["error"] == 29: # TODO: dependency injection.
                gevent.sleep(self.wait_window.total_seconds(), ref=True)

        except Exception:
            traceback.print_exc()

        return response

    def _throttle(self):
        self.now = datetime.datetime.now(datetime.UTC)
        if not self.burst_start:
            self.burst_start = datetime.datetime.now(datetime.UTC)

        if self.now < self.burst_start + self.burst_window:
            return datetime.timedelta(0)

        self.burst_start = None
        return self.wait_window
