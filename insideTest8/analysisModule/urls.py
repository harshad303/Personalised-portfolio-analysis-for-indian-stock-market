from django.urls import path
from . import views


urlpatterns = [
    path("showAnalysis", views.showAnalysis, name='showAnalysis'),
    path("showStocks", views.showStocks, name='showStocks'),

]