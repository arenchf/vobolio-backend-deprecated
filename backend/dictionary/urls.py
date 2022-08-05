from django import views
from django.urls import path
from .views import DictionaryDetailView, DictionaryView


urlpatterns = [
    path('dictionaries/', DictionaryView.as_view(), name='dictionaries'),
    path('dictionaries/<int:pk>/',
         DictionaryDetailView.as_view(), name="dictionary"),
]
