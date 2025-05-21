from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from account.forms import RegisterForm, LoginForm, UserUpdateForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pwd = form.cleaned_data["password"]
            user.set_password(pwd)
            user.save()

            # Connexion automatique
            user = authenticate(username=user.username, password=pwd)
            login(request, user)

            messages.success(request, "✅ Inscription réussie. Vous êtes connecté.")
            return redirect("account:profile")
        else:
            messages.error(request, "❌ Erreur dans le formulaire.")
    else:
        form = RegisterForm()

    return render(request, "account/register.html", {
        "form": form,
        "title": "📝 Inscription",
    })

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "ℹ️ Vous êtes déjà connecté.")
        return redirect("account:profile")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user:
                login(request, user)
                messages.success(request, "✅ Connexion réussie.")
                return redirect("account:profile")
            else:
                messages.error(request, "❌ Identifiants invalides.")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {
        "form": form,
        "title": "🔐 Connexion",
    })

def logout_view(request):
    logout(request)
    messages.info(request, "✅ Vous avez été déconnecté.")
    return redirect("account:login")

@login_required
def profile_view(request):
    return render(request, "account/profile.html", {
        "title": "👤 Mon profil",
        "user": request.user,
    })

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profil mis à jour avec succès.")
            return redirect("account:profile")
        messages.error(request, "❌ Une erreur est survenue.")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "account/edit_profile.html", {
        "form": form,
        "title": "✏️ Modifier le profil"
    })

from django.contrib.auth import logout

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # déconnecter l'utilisateur AVANT suppression
        user.delete()
        messages.success(request, "🗑 Votre compte a été supprimé avec succès.")
        return redirect("home")

    return render(request, "account/delete_account.html", {
        "title": "🗑 Supprimer mon compte"
    })
