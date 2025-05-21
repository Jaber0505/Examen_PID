from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogue.forms import ArtistTypeForm
from catalogue.models import ArtistType

@login_required
def create(request):
    form = ArtistTypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Participation artistique créer.")
        return redirect('catalogue:artist-type-index')  # à adapter à ton URL
    return render(request, "artist_type/form.html", {
        "form": form,
        "title": "➕ Associer un type à un artiste"
    })

@login_required
def index(request):
    from catalogue.models import ArtistType
    artist_types = ArtistType.objects.select_related("artist", "type")
    return render(request, "artist_type/index.html", {
        "artist_types": artist_types,
        "title": "👥 Types d'artistes"
    })

@login_required
def edit(request, id):
    artist_type = get_object_or_404(ArtistType, pk=id)
    form = ArtistTypeForm(request.POST or None, instance=artist_type)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Participation artistique modifier.")
        return redirect('catalogue:artist-type-index')
    return render(request, "artist_type/form.html", {
        "form": form,
        "title": "✏️ Modifier une association artiste/type"
    })

def delete(request, id):
    artist_type = get_object_or_404(ArtistType, pk=id)

    if request.method == "POST":
        artist_type.delete()
        messages.success(request, "🗑 Association artiste/type supprimée.")
        return redirect('catalogue:artist-type-index')

    return render(request, "artist_type/delete.html", {
        "artist_type": artist_type,
        "title": f"🗑 Supprimer l’association {artist_type}"
    })
