import src.obj
import pytest


class Test:
    @pytest.fixture
    def obj(self):
        return src.obj.ServiceAPI("https://api.hh.ru")

    def test_get_data(self, obj):
        assert obj.get_data() == {'message': 'Hello World'}