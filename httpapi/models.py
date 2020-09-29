import os
from enum import Enum
from typing import Any
from typing import Dict, Text, Union, Callable, List

from pydantic import BaseModel, Field
from pydantic import HttpUrl

Name = Text
Url = Text
BaseUrl = Union[HttpUrl, Text]
VariablesMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]
Headers = Dict[Text, Text]
Cookies = Dict[Text, Text]
Verify = bool
Hooks = List[Union[Text, Dict[Text, Text]]]
Export = List[Text]
Validators = List[Dict]
Env = Dict[Text, Any]


class HTTPMethodEnum(Text, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class TestCaseConfig(BaseModel):
    name: Name
    verify: Verify = False
    base_url: BaseUrl= ""
    variables: Union[VariablesMapping, Text] = {}
    parameters: Union[VariablesMapping, Text] = {}
    export: Export = []
    path: Text = None
    weight: int = 1


class TestCaseRequest(BaseModel):
    name: Name
    url: Url
    params: Dict[Text, Text] = {}
    headers: Headers = {}
    req_json: Union[Dict, List, Text] = Field(None, alias='json')
    data: Union[Text, Dict[Text, Any]] = None
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = False
    verify: Verify = False
    upload = Dict = {}


class TestCaseStep(BaseModel):
    name: Name
    request: Union[TestCaseRequest, None] = None
    testcase: Union[Text, Callable, None] = None
    variables: VariablesMapping = {}
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []
    extract: VariablesMapping = {}
    export: Export = []
    validators: Validators = Field([], alias='validate')
    validate_script: List[Text] = []


class TestCase(BaseModel):
    config: TestCaseConfig
    teststeps: List[TestCaseStep]


class AddressData(BaseModel):
    pass


class RequestData(BaseModel):
    method: HTTPMethodEnum = HTTPMethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: Union[Text, bytes, Dict, List, None] = {}


class ResponseData(BaseModel):
    status_code: int
    headers: Dict
    cookies: Cookies
    encoding: Union[Text, None] = None
    content_type: Text
    body: Union[Text, bytes, Dict]


class ReqResData(BaseModel):
    request: RequestData
    response: ResponseData
