from django.urls import path
from . import views

app_name = 'contests'
urlpatterns = [
    path('events/', views.events_view, name='events'),
    path('trials/<int:event_id>/', views.trials_view, name='trials'),
    path('publications/<int:trial_id>/', views.publications_view, name='publications'),
    path('manage-events/', views.manage_events, name='manage_events'),
    path('manage-events/<int:event_id>/', views.manage_event_detail, name='manage_event_detail'),
    path('manage-trials/<int:trial_id>/submissions/', views.manage_trial_submissions, name='manage_trial_submissions'),
    path('manage-submissions/<int:submission_id>/', views.manage_submission_detail, name='manage_submission_detail'),
    path('vote/<int:submission_id>/', views.vote_submission, name='vote_submission'),
]