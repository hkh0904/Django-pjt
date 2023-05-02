from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/<str:name>/', views.recommended, name='recommended'),
    path('genre_list/', views.genre_list, name='genre_list'),
    
]
