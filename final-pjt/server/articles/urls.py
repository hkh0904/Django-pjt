from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_create),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/like/', views.article_likes),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('<int:article_pk>/comments/', views.comment_create),
    path('replys/', views.reply_list),
    path('replys/<int:reply_pk>/', views.reply_detail),
    path('<int:comment_pk>/replys/', views.reply_create),
]