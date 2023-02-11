from django.urls import path

from . import views

app_name = 'get_vendors'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:vendor_id>/', views.detail, name='detail'),
    path('<int:vendor_id>/distance/', views.distance, name='distance'),
    path('<int:vendor_id>/hours/', views.hours, name='hours'),
]