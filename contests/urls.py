# C:\Users\T.SHIGARAKI\Desktop\ODC_CONTEST\contests\urls.py
from django.urls import path
from . import views

app_name = 'contests'
urlpatterns = [
    path('events/', views.events_view, name='events'),
    path('trials/<int:event_id>/', views.trials_view, name='trials'),
    path('publications/<int:trial_id>/', views.publications_view, name='publications'),
    path('manage-events/', views.manage_events, name='manage_events'),
]