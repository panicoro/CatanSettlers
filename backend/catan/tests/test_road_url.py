import pytest
from django.urls import reverse, resolve


class TestUrls:
    def test_BuildRoad_url(self):
        path = reverse('BuildRoad', kwargs={'pk': 1})
        assert resolve(path).view_name == 'BuildRoad'
