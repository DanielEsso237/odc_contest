from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from .models import Event, Trial, Competitor, Submission, SubmissionMedia, Vote
from accounts.models import User

@login_required
def events_view(request):
    events = Event.objects.all().order_by('-start_date')
    # Ajout du gagnant global pour chaque événement terminé
    for event in events:
        if event.end_date < timezone.now():
            # Récupérer les soumissions publiées de l'événement avec le nombre de votes
            submissions = Submission.objects.filter(
                trial__event=event, is_published=True
            ).annotate(vote_count=models.Count('votes')).values('competitor', 'vote_count')
            
            # Agréger les votes par compétiteur
            competitor_votes = {}
            for submission in submissions:
                competitor_id = submission['competitor']
                vote_count = submission['vote_count']
                if competitor_id in competitor_votes:
                    competitor_votes[competitor_id] += vote_count
                else:
                    competitor_votes[competitor_id] = vote_count
            
            # Trouver le compétiteur avec le plus de votes
            if competitor_votes:
                winning_competitor_id = max(competitor_votes, key=competitor_votes.get)
                winning_competitor = Competitor.objects.get(id=winning_competitor_id)
                event.winner = winning_competitor.user if competitor_votes[winning_competitor_id] > 0 else None
            else:
                event.winner = None
        else:
            event.winner = None
    return render(request, 'contests/events.html', {'events': events})

@login_required
def trials_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST' and 'create_trial' in request.POST:
        if request.user.role.lower() != 'modo':
            messages.error(request, "Vous n'avez pas les permissions nécessaires.")
            return redirect('contests:trials', event_id=event.id)
        
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if not title:
            messages.error(request, "Le titre de l'épreuve est obligatoire.")
        else:
            order = Trial.objects.filter(event=event).count() + 1
            try:
                Trial.objects.create(
                    event=event,
                    title=title,
                    description=description,
                    order=order
                )
                messages.success(request, f"Épreuve '{title}' créée avec succès !")
            except Exception as e:
                messages.error(request, f"Erreur lors de la création de l'épreuve : {str(e)}")
        
        return redirect('contests:trials', event_id=event.id)
    
    trials = Trial.objects.filter(event=event).order_by('order')
    for trial in trials:
        if event.end_date < timezone.now():
            winning_submission = Submission.objects.filter(trial=trial, is_published=True).annotate(
                vote_count=models.Count('votes')
            ).order_by('-vote_count').first()
            trial.winner = winning_submission.competitor.user if winning_submission else None
        else:
            trial.winner = None
    
    return render(request, 'contests/trials.html', {'event': event, 'trials': trials})

@login_required
def publications_view(request, trial_id):
    trial = get_object_or_404(Trial, id=trial_id)
    submissions = Submission.objects.filter(trial=trial, is_published=True).order_by('-published_at')
    for submission in submissions:
        submission.has_voted = Vote.objects.filter(submission=submission, member=request.user).exists()
        submission.vote_count = submission.votes.count()
    return render(request, 'contests/publications.html', {'trial': trial, 'submissions': submissions})

@login_required
def vote_submission(request, submission_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    submission = get_object_or_404(Submission, id=submission_id, is_published=True)
    user = request.user
    
    existing_vote = Vote.objects.filter(submission=submission, member=user).first()
    
    if existing_vote:
        existing_vote.delete()
        has_voted = False
    else:
        try:
            Vote.objects.create(submission=submission, member=user)
            has_voted = True
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    vote_count = submission.votes.count()
    
    return JsonResponse({
        'success': True,
        'has_voted': has_voted,
        'vote_count': vote_count
    })

@login_required
def manage_events(request):
    if request.user.role.lower() != 'modo':
        return redirect('accounts:home')
    
    if request.method == 'POST':
        if 'create_event' in request.POST:
            title = request.POST['title']
            description = request.POST['description']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            Event.objects.create(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                created_by=request.user
            )
            messages.success(request, "Événement créé !")
        elif 'create_trial' in request.POST:
            event_id = request.POST['event_id']
            title = request.POST['title']
            description = request.POST['description']
            order = Trial.objects.filter(event_id=event_id).count() + 1
            Trial.objects.create(
                event_id=event_id,
                title=title,
                description=description,
                order=order
            )
            messages.success(request, "Épreuve créée !")
        elif 'register_competitor' in request.POST:
            username = request.POST['username']
            event_id = request.POST['event_id']
            try:
                user = User.objects.get(username=username, role='member')
                user.role = 'participant'
                user.save()
                event = Event.objects.get(id=event_id)
                Competitor.objects.get_or_create(user=user, event=event, registered_by=request.user)
                messages.success(request, f"{username} transformé en participant et enregistré !")
            except User.DoesNotExist:
                messages.error(request, f"Utilisateur '{username}' non trouvé ou n'a pas le rôle 'member'.")
            except Event.DoesNotExist:
                messages.error(request, "Événement non trouvé.")
        elif 'delete_competitor' in request.POST:
            competitor_id = request.POST['competitor_id']
            try:
                competitor = Competitor.objects.get(id=competitor_id)
                user = competitor.user
                user.role = 'member'
                user.save()
                competitor.delete()
                messages.success(request, "Concurrente supprimée !")
            except Competitor.DoesNotExist:
                messages.error(request, "Concurrente non trouvée.")
        elif 'publish_submission' in request.POST:
            submission_id = request.POST['submission_id']
            try:
                submission = Submission.objects.get(id=submission_id)
                submission.is_published = True
                submission.published_by = request.user
                submission.save()
                messages.success(request, "Soumission publiée !")
            except Submission.DoesNotExist:
                messages.error(request, "Soumission non trouvée.")
    
    events = Event.objects.filter(created_by=request.user)
    members = User.objects.filter(role='member')
    submissions = Submission.objects.filter(is_published=False)
    competitors = Competitor.objects.all()

    return render(request, 'contests/manage_events.html', {
        'user': request.user,
        'events': events,
        'members': members,
        'submissions': submissions,
        'competitors': competitors
    })

@login_required
def manage_event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user.role.lower() != 'modo' or event.created_by != request.user:
        return redirect('accounts:home')
    
    if request.method == 'POST' and 'create_trial' in request.POST:
        title = request.POST['title']
        description = request.POST['description']
        order = Trial.objects.filter(event=event).count() + 1
        Trial.objects.create(
            event=event,
            title=title,
            description=description,
            order=order
        )
        messages.success(request, "Épreuve créée avec succès !")
        return redirect('contests:trials', event_id=event.id)

    trials = Trial.objects.filter(event=event).order_by('order')
    competitors = Competitor.objects.filter(event=event)
    return render(request, 'contests/manage_event_detail.html', {
        'event': event,
        'trials': trials,
        'competitors': competitors
    })

@login_required
def manage_trial_submissions(request, trial_id):
    trial = get_object_or_404(Trial, id=trial_id)
    if request.user.role.lower() != 'modo' or trial.event.created_by != request.user:
        return redirect('accounts:home')
    
    submissions = Submission.objects.filter(trial=trial, is_published=False)
    return render(request, 'contests/manage_trial_submissions.html', {
        'trial': trial,
        'submissions': submissions
    })

@login_required
def manage_submission_detail(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    trial = submission.trial
    if request.user.role.lower() != 'modo' or trial.event.created_by != request.user:
        return redirect('accounts:home')
    
    if request.method == 'POST':
        if 'publish' in request.POST:
            moderator_text = request.POST.get('moderator_text', '')
            submission.moderator_text = moderator_text
            submission.is_published = True
            submission.published_by = request.user
            submission.save()
            messages.success(request, "Soumission publiée avec succès !")
            return redirect('contests:publications', trial_id=trial.id)
        elif 'reject' in request.POST:
            submission.delete()
            messages.success(request, "Soumission rejetée et supprimée !")
            return redirect('contests:manage_trial_submissions', trial_id=trial.id)

    return render(request, 'contests/manage_submission_detail.html', {
        'submission': submission,
        'trial': trial
    })