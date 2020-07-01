import pytest
from django.urls import reverse, resolve


class TestUrls:
    def test_BoardInfo_url(self):
        path = reverse('BoardInfo', kwargs={'pk': 1})
        assert resolve(path).view_name == 'BoardInfo'

    def test_Boards_url(self):
        path = reverse('Boards')
        assert resolve(path).view_name == 'Boards'
