from django.urls import path

from . import views

urlpatterns = [
    path("date/<str:date>/", views.index, name="new_index"),
]
