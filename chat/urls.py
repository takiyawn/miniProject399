from django.urls import path
from . import views

"""
root URL routing    
"""


urlpatterns = [
    path("", views.home, name="home"),
    path("ask/", views.ask, name="ask"),
]

