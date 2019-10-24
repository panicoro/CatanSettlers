import pytest
from django.urls import reverse, resolve
class TestUrls:
    def test_BuildSettlement_url(self):
        path = reverse('BuildSettlement', kwargs={'pk': 1})
        assert resolve(path).view_name == 'BuildSettlement'
