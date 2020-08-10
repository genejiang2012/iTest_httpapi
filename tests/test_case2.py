import pytest


class TestCase2():
    @pytest.mark.xfail(condition=lambda: True, reason='this test is expecting failure')
    def test_xfail_expected_failure(self):
        """this test is an xfail that will be marked as expected failure"""
        assert False