import pytest
from django.urls import reverse, resolve


class TestUrls:
    def test_Register_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'
