from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Trial, Submission

@login_required
def events_view(request):
    events = Event.objects.all().order_by('-start_date')  # Plus récents en premier
    return render(request, 'contests/events.html', {'events': events})

@login_required
def trials_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    trials = Trial.objects.filter(event=event).order_by('order')
    return render(request, 'contests/trials.html', {'event': event, 'trials': trials})

@login_required
def publications_view(request, trial_id):
    trial = get_object_or_404(Trial, id=trial_id)
    submissions = Submission.objects.filter(trial=trial, is_published=True).order_by('-published_at')
    return render(request, 'contests/publications.html', {'trial': trial, 'submissions': submissions})