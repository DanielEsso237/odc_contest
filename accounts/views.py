from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from contests.models import Trial, Competitor, Submission, SubmissionMedia
from django import forms

class MultipleFileInput(forms.FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs.update({'multiple': True})
        self.attrs = attrs

class SubmissionForm(forms.ModelForm):
    media_files = forms.FileField(
        widget=MultipleFileInput(attrs={
            'accept': '.jpg,.jpeg,.png,.mp4,.mov',
            'class': 'form-control'
        }),
        help_text="Sélectionnez une ou plusieurs photos/vidéos (.jpg, .jpeg, .png, .mp4, .mov)",
        required=True
    )
    
    class Meta:
        model = Submission
        fields = ['trial', 'description']
        widgets = {
            'trial': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, competitor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if competitor and hasattr(competitor, 'event'):
            self.fields['trial'].queryset = Trial.objects.filter(event=competitor.event)
        else:
            self.fields['trial'].queryset = Trial.objects.none()

@login_required
def submit_entry(request):
    if request.user.role.lower() != 'participant':
        return redirect('accounts:home')
    
    competitor = get_object_or_404(Competitor, user=request.user)
    trials = Trial.objects.filter(event=competitor.event)

    if request.method == 'POST':
        form = SubmissionForm(competitor, request.POST, request.FILES)
        if form.is_valid():
            trial = form.cleaned_data['trial']
            
            if Submission.objects.filter(competitor=competitor, trial=trial).exists():
                messages.error(request, "Vous avez déjà soumis une entrée pour cette épreuve. Contactez un modérateur si nécessaire.")
                return redirect('accounts:submit_entry')
            
            files = request.FILES.getlist('media_files')
            if not files:
                messages.error(request, "Veuillez sélectionner au moins un fichier média.")
                return render(request, 'accounts/submit_entry.html', {'form': form, 'trials': trials})
            
            submission = form.save(commit=False)
            submission.competitor = competitor
            submission.save()
            
            valid_files_count = 0
            for i, file in enumerate(files):
                import os
                file_extension = os.path.splitext(file.name)[1].lower()
                valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
                
                if file_extension not in valid_extensions:
                    messages.warning(request, f"Le fichier {file.name} a été ignoré (extension non autorisée).")
                    continue
                
                media_obj = SubmissionMedia.objects.create(
                    submission=submission,
                    media=file,
                    order=i
                )
                valid_files_count += 1
            
            if valid_files_count > 0:
                messages.success(request, f"Soumission envoyée avec succès avec {valid_files_count} fichier(s) ! Attends la validation du modérateur.")
                return redirect('accounts:home')
            else:
                submission.delete()
                messages.error(request, "Aucun fichier valide n'a été trouvé. Veuillez vérifier les formats autorisés.")
                
        else:
            messages.error(request, "Erreur dans la soumission. Vérifie tes données.")
    else:
        form = SubmissionForm(competitor=competitor)  
    
    return render(request, 'accounts/submit_entry.html', {'form': form, 'trials': trials})

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['email']  
        password = request.POST['password']
        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('accounts:home')
        else:
            messages.error(request, "Email/Utilisateur ou mot de passe incorrect.")
    return render(request, 'accounts/login.html')

def register_view(request):
    from .forms import UserRegistrationForm
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.backend = 'accounts.backends.EmailOrUsernameModelBackend'
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue !")
            return redirect('accounts:home')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifie tes données.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect('accounts:login')

@login_required
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/home.html', {'user': request.user})

def events_view(request):
    return render(request, 'accounts/events.html', {'user': request.user})

def notifications_view(request):
    return render(request, 'accounts/notifications.html', {'user': request.user})

def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})