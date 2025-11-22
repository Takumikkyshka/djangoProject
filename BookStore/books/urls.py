from django.urls import path
from . import views

# Пространство имен приложения - позволяет уникально идентифицировать маршруты
# Например: 'books:home' вместо просто 'home'
app_name = 'books'

# Список всех URL-маршрутов приложения books
urlpatterns = [
    # Главная страница приложения
    path('', views.home, name='home'),
    
    # Маршруты для работы с авторами
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('authors/new/', views.author_create, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('authors/<int:pk>/delete/', views.author_delete, name='author_delete'),
    
    # Маршруты для работы с книгами
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/new/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
]