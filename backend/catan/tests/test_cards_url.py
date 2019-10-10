import pytest
from django.urls import reverse, resolve


class TestUrls: 
    def test_CardList_url(self):
        path = reverse('CardsList', kwargs={'pk': 1})
        assert resolve(path).view_name == 'CardsList'