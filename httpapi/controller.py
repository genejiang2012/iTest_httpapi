import json
import time

import requests
import urllib3
from loguru import logger
from requests import Request, Response
from requests.exceptions import (
    InvalidSchema,
    InvalidURL,
    MissingSchema,
    RequestException
)

from httpapi.models import SessionData, ResponseData, RequestData, ReqRespData

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiResponse(Response):
    def raise_for_status(self):
        if hasattr(self, "error") and self.error:
            raise self.error
        Response.raise_for_status(self)


class HttpSession(requests.Session):
    def __init__(self):
        super(HttpSession, self).__init__()
        self.data = SessionData()

    def update_last_req_resp_record(self, resp_obj):
        pass

    def request(self, method, url, name=None, **kwargs):
        self.data = SessionData()

        kwargs.setdefault("timeout", 120)

        kwargs["stream"] = True

        start_timestamp = time.time()

    def _send_request_safe_method(self, method, url, **kwargs):
        try:
            return requests.Session.request(self, method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as ex:
            resp = ApiResponse()
            resp.error = ex
            resp.status_code = 0
            resp.request = Request(method, url).prepare()
            return resp
