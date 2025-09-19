from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm  
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('home')  
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, "Inscription réussie ! Bienvenue !")
            return redirect('home')  
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifie tes données.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})