import pytest
from django.urls import reverse, resolve


class TestUrls:
    def test_Token_url(self):
        path = reverse('tokenObtainPair')
        assert resolve(path).view_name == 'tokenObtainPair'

    def test_Refresh_url(self):
        path = reverse('refreshToken')
        assert resolve(path).view_name == 'refreshToken'
