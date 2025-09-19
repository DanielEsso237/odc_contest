from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('modo-dashboard/', views.modo_dashboard, name='modo_dashboard'),
    path('home/', views.home_view, name='home'),
]