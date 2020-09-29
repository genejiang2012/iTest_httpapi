import json
import time

import requests
import urllib3
from loguru import logger
from requests import Request, Response

from httpapi.models import SessionData

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpSession(requests.Session):
    def __init__(self):
        super(HttpSession, self).__init__()
        self.data = SessionData()