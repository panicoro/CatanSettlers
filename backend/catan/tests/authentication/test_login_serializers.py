import pytest
from django.contrib.auth.models import User
from catan.serializers import SignupSerializer
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestSerializers:
    def test_get_token(self):
        user = mixer.blend(User, username="fedemarkco", password="fedemarkco")
        response = SignupSerializer.get_token(user)
        assert response is not None

    def test_validate(self):
        username = 'fedemarkco'
        email = 'fedemarkco@gmail.com'
        password = 'fedemarkco'
        User.objects.create_user(username, email, password)
        attrs = {
                    "password": "fedemarkco",
                    "username": "fedemarkco"
                }
        response = SignupSerializer.validate(SignupSerializer, attrs=attrs)
        assert 'access' in response
