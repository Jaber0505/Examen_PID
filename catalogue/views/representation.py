from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from catalogue.models import Representation, Reservation
from catalogue.forms import RepresentationForm

@login_required
def index(request):
    representations = Representation.objects.select_related('show', 'location').all()
    return render(request, 'representation/index.html', {
        'representations': representations,
        'title': "Liste des représentations"
    })

@login_required
def show(request, id):
    representation = get_object_or_404(Representation, id=id)
    has_reservation = Reservation.objects.filter(user=request.user, representation=representation).exists()

    return render(request, 'representation/show.html', {
        'representation': representation,
        'has_reservation': has_reservation,
        'now': timezone.now(),
        'title': "Détail de la représentation"
    })

@login_required
def create(request):
    form = RepresentationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('catalogue:representation-index')
    return render(request, 'representation/form.html', {
        'form': form,
        'title': "➕ Ajouter une représentation"
    })

@login_required
def edit(request, id):
    representation = get_object_or_404(Representation, id=id)
    form = RepresentationForm(request.POST or None, instance=representation)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('catalogue:representation-show', id=representation.id)
    return render(request, 'representation/form.html', {
        'form': form,
        'representation': representation,
        'title': f"✏️ Modifier la représentation du {representation.schedule.strftime('%d/%m/%Y %H:%M')}"
    })

@login_required
def delete(request, id):
    representation = get_object_or_404(Representation, id=id)
    if request.method == 'POST':
        representation.delete()
        return redirect('catalogue:representation-index')
    return render(request, 'representation/delete.html', {
        'representation': representation,
        'title': f"🗑 Supprimer la représentation du {representation.schedule.strftime('%d/%m/%Y %H:%M')}"
    })
