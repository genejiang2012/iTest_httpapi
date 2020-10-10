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

from loguru import logger

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
        response = self._send_request_safe_method(method, url, **kwargs)
        response_time_ms = round((time.time() - start_timestamp) * 1000, 2)

        try:
            client_ip, client_port = response.raw.connection.sock.getsockname()
            self.data.address.client_ip = client_ip
            self.data.address.client_port = client_port
            logger.debug(f"client IP:{client_ip}, Port:{client_port}")
        except AttributeError as ex:
            logger.warning(f"failed to get the client address info:{ex}")

        try:
            server_ip, server_port = response.raw.connection.sock.getsockname()
            self.data.address.client_ip = server_ip
            self.data.address.client_port = server_port
            logger.debug(f"server IP:{server_ip}, Port:{server_port}")
        except AttributeError as ex:
            logger.warning(f"failed to get the server address info:{ex}")

        # get the length of the response content
        content_size = int(dict(response.headers).get("content-length") or 0)

        # record the consumed time
        self.data.stat.response_time_ms = response_time_ms
        self.data.stat.elapsed_ms = response.elapsed.microseconds / 1000.0
        self.data.stat.content_size = content_size

        # record request and response histories, include 30X redirection
        response_list = response.history + [response]
        self.data.req_resps = [
            get_req_resp_record(resp_obj) for resp_obj in response_list
        ]

        try:
            response.raise_for_status()
        except RequestException as ex:
            logger.error(f"{str(ex)}")
        else:
            logger.info(
                f"status_code: {response.status_code}, "
                f"response_time(ms): {response_time_ms} ms, "
                f"response_length: {content_size} bytes"
            )

        return response

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


def get_req_resp_record(resp_obj: Response) -> ReqRespData:
    def log_print(req_or_resp, r_type):
        msg = f"\n================== {r_type} details ==================\n"
        for key, value in req_or_resp.dict().items():
            if isinstance(value, dict):
                value = json.dumps(value, indent=4)
            msg += "{:<8} : {}\n".format(key, value)
        logger.debug(msg)

    # record the actual request info
    request_headers = dict(resp_obj.request.headers)
    request_cookies = resp_obj.request._cookies.get_dict()

    request_body = resp_obj.request.body

    if request_body is not None:
        try:
            request_body = json.loads(request_body)
        except json.JSONDecodeError:
            # str: a=1&b=2
            pass
        except UnicodeDecodeError:
            # bytes/bytearray: request body in protobuf
            pass
        except TypeError:
            # neither str nor bytes/bytearray, e.g. <MultipartEncoder>
            pass

        request_content_type = request_headers.get("content-type")
        if request_content_type and "multipart/form-data" in request_content_type:
            # upload file type
            request_body = "upload file stream (OMITTED)"

    request_data = RequestData(
        method=resp_obj.request.method,
        url=resp_obj.request.url,
        headers=request_headers,
        cookies=request_cookies,
        body=request_body,
    )

    # record response data
    resp_headers = dict(resp_obj.headers)
    lower_resp_headers = resp_headers
    content_type = lower_resp_headers.get("content-type", "")

    if "image" in content_type:
        # response is image type, record bytes content only
        response_body = resp_obj.content
    else:
        try:
            # try to record json data
            response_body = resp_obj.json()
        except ValueError:
            # only record at most 512 text charactors
            resp_text = resp_obj.text
            response_body = resp_text

    response_data = ResponseData(
        status_code=resp_obj.status_code,
        cookies=resp_obj.cookies or {},
        encoding=resp_obj.encoding,
        headers=resp_headers,
        content_type=content_type,
        body=response_body,
    )

    req_resp_data = ReqRespData(request=request_data, response=response_data)
    return req_resp_data