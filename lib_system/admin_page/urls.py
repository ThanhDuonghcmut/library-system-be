from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashBoard, name='dashboard'),
    path('books/', views.books, name='books'),
    path('category/', views.category, name='category')
]
