from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('shows/', views.shows, name='shows'),
    path('shows/new/', views.new_show, name='new_show'),
    path('shows/create/', views.create_show, name='create_show')
]
