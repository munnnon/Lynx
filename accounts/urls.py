from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name = 'login'),
    path('settings/', views.account_settings_view, name = 'account_settings'),
    path('password_change/', views.change_password_view, name='password_change'),
    path('email_change/', views.change_email, name='email_change'),
    path('username_change/', views.change_username, name='username_change'),
]
