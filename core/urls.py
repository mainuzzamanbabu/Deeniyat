from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('submit-task/', views.submit_daily_task, name='submit_daily_task'),
    path('submit-donation/', views.submit_donation_verification, name='submit_donation_verification'),
    path('accounts-dashboard/', views.approve_donation, name='approve_donation'),
    path('superadmin-dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
]
