from django.urls import path
from . import views


urlpatterns = [
    path("showgraph", views.showgraph, name='showgraph'),
    path("showPort", views.showPort, name='showPort'),
    path("viewportfolio", views.viewportfolio, name='viewportfolio'),

]