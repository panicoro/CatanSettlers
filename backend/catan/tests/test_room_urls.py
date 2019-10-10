from django.urls import reverse, resolve


class TestUrls:
    def test_listRoom_url(self):
        path = reverse('list_rooms')
        assert resolve(path).view_name == 'list_rooms'

    def test_joinRoom_url(self):
        path = reverse('join_room', kwargs={'pk': 1})
        assert resolve(path).view_name == 'join_room'
