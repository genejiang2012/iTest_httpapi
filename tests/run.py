import pytest
import os

if __name__ == '__main__':
    pytest.main(["-sq",
                 "--alluredir", 'results'])
    os.system("allure generate -c results -o report")
