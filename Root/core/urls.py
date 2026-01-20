from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.base, name='base'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forget, name='forgot-password'),
    path("reset/<uidb64>/<token>/", views.reset_password_confirm, name="password_reset_confirm"),
    path('register/', views.register, name='register'),
]