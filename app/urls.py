from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('shows/', views.shows, name='shows'),
    path('shows/<int:show_id>/', views.view_show, name='view_show'),
    path('shows/<int:show_id>/edit/', views.edit_show, name='edit_show'),
    path('shows/<int:show_id>/update/', views.update_show, name='update_show'),
    path('shows/<int:show_id>/delete/', views.delete_show, name='delete_show'),
    path('shows/new/', views.new_show, name='new_show'),
    path('shows/create/', views.create_show, name='create_show')
]
