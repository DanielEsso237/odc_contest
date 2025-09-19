from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            if user.is_superuser:  
                return redirect('/admin/')  
            elif user.role.lower() == 'modo': 
                return redirect('accounts:modo_dashboard')  
            else:  # Membres et participants
                return redirect('accounts:home') 
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'accounts/login.html')

def register_view(request):
    from .forms import UserRegistrationForm
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue !")
            return redirect('accounts:home')
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifie tes données.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def modo_dashboard(request):
    if not request.user.is_authenticated or request.user.role.lower() != 'modo':  
        return redirect('accounts:login') 
    return render(request, 'accounts/modo_dashboard.html', {'user': request.user})

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  
    return render(request, 'accounts/home.html', {'user': request.user})