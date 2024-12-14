from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/date/(?P<date>\d{4}-\d{2}-\d{2})/$", consumers.ChatConsumer.as_asgi()),
]