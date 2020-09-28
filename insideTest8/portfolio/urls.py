from django.urls import path
from . import views


urlpatterns = [
    path("showportfolio", views.showportfolio, name='showportfolio'),
    path("removeportfolio", views.removeportfolio, name='removeportfolio'),
    path("enterportfolio",views.enterportfolio,name='enterportfolio')
]