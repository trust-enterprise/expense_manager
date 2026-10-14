from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:id>/', views.delete_expense, name='delete'),
    path('edit/<int:id>/', views.edit_expense, name='edit'),
]
