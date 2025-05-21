from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Role, CustomUser

def user_has_admin_role(user):
    return user.is_authenticated and user.roles.filter(role='Admin').exists()

@login_required
@user_passes_test(user_has_admin_role)
def dashboard_view(request):
    users = CustomUser.objects.all()
    return render(request, "account/dashboard.html", {
        "users": users,
        "title": "Dashboard Admin - Liste des utilisateurs"
    })
    
@login_required
def dashboard(request):
    # page d'accueil du dashboard
    if not request.user.is_admin:
        messages.error(request, "Accès refusé")
        return redirect("home")

    return render(request, "account/dashboard.html", {
        "title": "Dashboard Admin",
    })

@login_required
def dashboard_roles(request):
    if not request.user.is_admin:
        messages.error(request, "Accès refusé")
        return redirect("home")

    roles = Role.objects.all()
    users = CustomUser.objects.all().prefetch_related('roles')

    return render(request, "account/dashboard_roles.html", {
        "roles": roles,
        "users": users,
        "title": "Gestion des rôles",
    })

@login_required
def dashboard_edit_role(request, user_id):
    if not request.user.is_admin:
        messages.error(request, "Accès refusé")
        return redirect("home")

    user = get_object_or_404(CustomUser, id=user_id)
    roles = Role.objects.all()

    if request.method == "POST":
        selected_roles = request.POST.getlist("roles")
        # Met à jour les rôles
        user.roles.set(Role.objects.filter(role__in=selected_roles))
        messages.success(request, f"Rôles mis à jour pour {user.username}.")
        return redirect("account:dashboard-roles")

    return render(request, "account/dashboard_edit_role.html", {
        "user_to_edit": user,
        "roles": roles,
        "title": f"Modifier les rôles de {user.username}"
    })
