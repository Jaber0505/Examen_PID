from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from catalogue.models import Artist, ArtistTypeShow
from catalogue.forms import ArtistForm

def index(request):
    artists = Artist.objects.all()
    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': "🧑‍🎤 Artistes"
    })

def show(request, artist_id):
    artist = get_object_or_404(Artist.objects.select_related('troupe'), pk=artist_id)
    types = artist.artiste_type.select_related("type")

    participations = ArtistTypeShow.objects.filter(artist_type__artist=artist).select_related(
        "artist_type__type", "show"
    )

    return render(request, "artist/show.html", {
        "artist": artist,
        "types": types,
        "participations": participations,
        "title": f"🎭 {artist}"
    })


def create(request):
    if request.method == "POST":
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Artiste ajouté avec succès.")
            return redirect('catalogue:artist-index')
        else:
            messages.error(request, "❌ Une erreur est survenue. Veuillez vérifier le formulaire.")
    else:
        form = ArtistForm()

    return render(request, 'artist/form.html', {
        'form': form,
        'title': "Ajouter un artiste"
    })

@login_required
def edit(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    # Seulement admin peut modifier l'affiliation troupe
    is_admin = request.user.is_authenticated and request.user.is_admin

    if request.method == "POST":
        if is_admin:
            form = ArtistForm(request.POST, instance=artist)
        else:
            # Formulaire sans troupe pour les non-admin
            form = ArtistForm(request.POST, instance=artist)
            form.fields.pop('troupe')

        if form.is_valid():
            form.save()
            return redirect('catalogue:artist-show', artist.id)
    else:
        if is_admin:
            form = ArtistForm(instance=artist)
        else:
            form = ArtistForm(instance=artist)
            form.fields.pop('troupe')

    return render(request, 'artist/form.html', {
        'form': form,
        'title': f"✏️ Modifier l’artiste : {artist.first_name} {artist.last_name}",
        'is_admin': is_admin,
    })

def delete(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    if request.method == "POST":
        artist.delete()
        messages.warning(request, "✅ Artiste supprimé.")
        return redirect('catalogue:artist-index')

    return render(request, 'artist/delete.html', {
        'artist': artist,
        'title': f"🗑 Supprimer {artist.first_name} {artist.last_name}"
    })
