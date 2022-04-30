from django import views
from django.urls import path
from .views import DictionaryView


urlpatterns = [
    path('dictionaries/', DictionaryView.as_view(), name='dictionaries'),
]