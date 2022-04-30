from django import views
from django.urls import path
from .views import CategoryView, WordView, CategoryDetailView, WordDetailView


urlpatterns = [
    path('dictionaries/<int:pk>/categories/', CategoryView.as_view(), name='categories'),
    path('dictionaries/<int:pk>/categories/<int:category_id>/',CategoryDetailView.as_view(), name="category detail"),
    path('dictionaries/<int:pk>/words/', WordView.as_view(), name="words"),
    path('dictionaries/<int:pk>/words/<int:word_id>/', WordDetailView.as_view(), name="words"),

]