from src import obj
import pytest


class TestHH:
    @pytest.fixture
    def test_obj(self):
        return obj.HH()

    def test_get_data(self, test_obj):
        test_code = test_obj.get_data(keyword='Разработчик')
        # print(test_obj.vacancies)
        assert type(test_obj.vacancies) == list