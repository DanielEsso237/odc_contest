
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('modo-dashboard/', views.modo_dashboard, name='modo_dashboard'),
    path('home/', views.home_view, name='home'),
    path('submit-entry/', views.submit_entry, name='submit_entry'),
    path('contests/events/', views.events_view, name='events'),
    path('notifications/', views.notifications_view, name='notifications'),  
    path('profile/', views.profile_view, name='profile'),  
    path('logout/', views.logout_view, name='logout'),
]