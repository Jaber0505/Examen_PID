from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from account.models import CustomUser
from account.forms import AssignRolesForm

# Optionnel: restreindre à superusers ou admin
def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def assign_roles_view(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "POST":
        form = AssignRolesForm(request.POST)
        if form.is_valid():
            roles = form.cleaned_data['roles']
            user.roles.set(roles)
            user.save()
            messages.success(request, f"Rôles mis à jour pour {user.username}.")
            return redirect('account:user_list')  # À adapter, par ex. liste des utilisateurs
    else:
        form = AssignRolesForm(initial={'roles': user.roles.all()})

    return render(request, "account/assign_roles.html", {
        "form": form,
        "user_obj": user,
        "title": f"Attribuer des rôles à {user.username}"
    })
    
@login_required
@user_passes_test(is_superuser)
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, "account/user_list.html", {
        "users": users,
        "title": "Liste des utilisateurs"
    })