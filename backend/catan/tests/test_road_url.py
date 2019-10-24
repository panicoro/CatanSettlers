import pytest
from django.urls import reverse, resolve


class TestUrls:
    def test_BuiltRoad_url(self):
        path = reverse('BuiltRoad', kwargs={'pk': 1})
        assert resolve(path).view_name == 'BuiltRoad'
