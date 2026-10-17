from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete'),
    path('edit/<int:expense_id>/', views.edit_expense, name='edit'),
    path('register/', views.register, name='register'), 
]
