from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forget, name='forgot-password'),
    path("reset/<uidb64>/<token>/", views.reset_password_confirm, name="password_reset_confirm"),
    path('register/', views.register, name='register'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('management-user/', views.manajement_user, name='management-user'),
    path('inventory/', views.inventory, name='inventory'),
]