from django.urls import path
from . import views


urlpatterns = [
    path("cummulative", views.cummulative, name='cummulative'),
]