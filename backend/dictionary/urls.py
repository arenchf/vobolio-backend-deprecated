from django import views
from django.urls import path
from .views import DictionaryDetailView, DictionaryView


urlpatterns = [
    path('users/<int:user_id>/dictionaries/',
         DictionaryView.as_view(), name='user_dictionaries'),
    path('users/<int:user_id>/dictionaries/<int:pk>/',
         DictionaryDetailView.as_view(), name="user_dictionary")
    # path('dictionaries/', DictionaryView.as_view(), name='dictionaries'),
    # path('dictionaries/<int:pk>/',
    #      DictionaryDetailView.as_view(), name="dictionary"),
]
