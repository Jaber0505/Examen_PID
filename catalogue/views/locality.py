from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalogue.models.locality import Locality
from catalogue.forms.locality_form import LocalityForm

def index(request):
    localities = Locality.objects.all()
    return render(request, "locality/index.html", {
        "title": "Liste des localités",
        "localities": localities,
    })

def show(request, locality_id):
    locality = get_object_or_404(Locality, pk=locality_id)
    return render(request, "locality/show.html", {
        "title": f"Fiche localité : {locality}",
        "locality": locality,
    })

def create(request):
    if request.method == "POST":
        form = LocalityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Localité ajoutée avec succès.")
            return redirect("catalogue:locality-index")
        messages.error(request, "❌ Erreur lors de la création.")
    else:
        form = LocalityForm()

    return render(request, "locality/form.html", {
        "title": "➕ Ajouter une localité",
        "form": form,
    })

def edit(request, locality_id):
    locality = get_object_or_404(Locality, pk=locality_id)

    if request.method == "POST":
        form = LocalityForm(request.POST, instance=locality)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Localité modifiée avec succès.")
            return redirect("catalogue:locality-show", form.instance.id)
        messages.error(request, "❌ Erreur lors de la modification.")
    else:
        form = LocalityForm(instance=locality)

    return render(request, "locality/form.html", {
        "title": f"✏️ Modifier : {locality}",
        "form": form,
    })

def delete(request, locality_id):
    locality = get_object_or_404(Locality, pk=locality_id)

    if request.method == "POST":
        locality.delete()
        messages.success(request, "🗑 Localité supprimée avec succès.")
        return redirect("catalogue:locality-index")

    return render(request, "locality/delete.html", {
        "title": f"🗑 Supprimer : {locality}",
        "locality": locality,
    })
