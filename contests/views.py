from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event, Trial, Submission

@login_required
def events_view(request):
    
    events = Event.objects.all().order_by('-start_date')  

    event_id = request.GET.get('event_id')
    trial_id = request.GET.get('trial_id')

    trials = []
    submissions = []

    if event_id:
        trials = Trial.objects.filter(event_id=event_id).order_by('order')
    
    if trial_id:
        submissions = Submission.objects.filter(trial_id=trial_id, is_published=True).order_by('-published_at')

    return render(request, 'contests/events.html', {
        'events': events,
        'trials': trials,
        'submissions': submissions,
        'selected_event': event_id,
        'selected_trial': trial_id,
    })