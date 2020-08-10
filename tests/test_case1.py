import pytest


class TestCase1:
    def test_success(self):
        """this test succeeds"""
        assert True

    def test_failure(self):
        """this test fails"""
        assert False

    def test_skip(self):
        """this test is skipped"""
        pytest.skip('for a reason!')

    def test_broken(self):
        raise Exception('oops')