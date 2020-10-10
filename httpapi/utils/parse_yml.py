import yaml

from httpapi.models import TestCaseStep

with open('../../testcases/000_login.yaml') as yml_file:
    yml_content = yaml.safe_load(yml_file)
    print(yml_content)
    print(yml_content['teststeps'])
