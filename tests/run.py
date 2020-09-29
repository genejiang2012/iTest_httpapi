import os

import pytest
import allure

if __name__ == '__main__':
    pytest.main(["-sq",
                 "--alluredir", 'results'])
    os.system("allure generate -c results -o report")
