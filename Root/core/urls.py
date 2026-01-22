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
    path('create/', views.create, name='create'),
    path('user/update/<int:id>/', views.update_user, name='update_user'),
    path('user/delete/<int:id>/', views.delete_user, name='delete_user'),

    path('inventory/', views.inventory, name='inventory'),
    path('inventory/create/', views.create_inv, name='create_inventory'),
    path('inventory/update/<int:id>/', views.update_inventory, name='update_inventory'),
    path('inventory/delete/<int:id>/', views.delete_inventory, name='delete_inventory'),
    path('inventory/buy/<int:id>/', views.buy, name='buy'),
]