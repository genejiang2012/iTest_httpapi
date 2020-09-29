import inspect
from typing import Text, Any, Union, Callable

from httpapi.models import (
    TestCaseConfig,
    TestCaseStep,
    TestCaseRequest,
    HTTPMethodEnum,
    TestCase
)


class Config:
    def __init__(self, name: Text):
        self.__name = name
        self.__variables = {}
        self.__base_url = ""
        self.__verify = False
        self.__export = []
        self.__weight = 1

        call_tracestack = inspect.stack()[1]
        self.__path = call_tracestack.filename

    @property
    def name(self) -> Text:
        return self.__name

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def path(self) -> Text:
        return self.__path

    def variables(self, **kw_variables) -> "Config":
        self.__variables.update(kw_variables)
        return self

    def base_url(self, base_url: Text) -> "Config":
        self.__base_url = base_url
        return self

    def verify(self, verify: bool) -> "Config":
        self.__verify = verify
        return self

    def export(self, *k_export_var_name: Text) -> "Config":
        self.__export.extend(k_export_var_name)
        return self

    def locust_weight(self, weight: int) -> "Config":
        self.__weight = weight
        return self

    def perform(self):
        pass


class RunRequest:
    def __init__(self, name: Text):
        self.__step_context = TestCaseStep(name=name)
