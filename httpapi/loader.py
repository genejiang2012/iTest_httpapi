import csv
import json
import yaml
import os
import sys
import types
from typing import Tuple, Dict, Text, List, Union, Callable

from loguru import logger
from pydantic import ValidationError


try:
    # PyYaml version >=5.1
    yaml.warnings({"YAMLLoadWarning": False})
except AttributeError:
    pass


def _load_yaml_file(yaml_file: Text) -> Dict:
    """
    load the yaml file
    """
    with open(yaml_file, mode='rb') as stream:
        try:
            yaml_content = yaml.load(stream)
        except yaml.YAMLError as ex:
            err_msg = f"YAMLError:\nfile:{yaml_file}\nerror:{ex}"
            logger.error(err_msg)
            raise FileNotFoundError

        return yaml_content


def _load_json_file(json_file: Text) -> Dict:
    """
    load the json file
    :param json_file: the path of the json file
    :return: get the content of the json file
    """
    with open(json_file, 'rb') as json_stream:
        try:
            json_content = json.load(json_stream)
        except json.JSONDecodeError as ex:
            err_msg = f"JSONError:\nfile:{json_file}\nerror:{ex}"
            logger.error(err_msg)
            raise FileExistsError

        return json_content


def load_test_file(test_file: Text) -> Dict:
    if not os.path.isfile(test_file):
        raise FileExistsError(f"test file is not existed:{test_file}")

    file_suffix = os.path.splitext(test_file)[1].lower()

    if file_suffix == ".json":
        test_file_content = _load_json_file(test_file)
    elif file_suffix in ['.yml', '.yaml']:
        test_file_content = _load_yaml_file(test_file)
    else:
        raise FileNotFoundError("testcase/test suite should be yaml or json format!")

    return test_file_content

