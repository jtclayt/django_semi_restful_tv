from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('shows', views.shows, name='shows')
]
