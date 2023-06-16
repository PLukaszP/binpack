from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    path('list/', views.list_view, name='list'),
    path('<int:id>', views.detail_view, name='detail'),
    path('<int:id>/del', views.delete_view, name='delete'),
]