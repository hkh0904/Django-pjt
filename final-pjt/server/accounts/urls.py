from django.urls import path
from . import views

urlpatterns = [
    path('userinfo/<int:user_pk>/', views.userinfo),
    path('follow/<int:user_pk>/', views.follow),
    path('update/<int:user_pk>/', views.update_user)
]
