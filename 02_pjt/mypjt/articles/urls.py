from django.urls import path
from . import views
app_name = 'articles'
urlpatterns = [
    path('<int:pk>', views.index, name='index'),
    path('/upload', views.upload, name='upload')
]
