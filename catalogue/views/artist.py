from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from catalogue.models import Artist, ArtistTypeShow, Troupe
from catalogue.forms import ArtistForm, ArtistTroupeForm

def index(request):
    artists = Artist.objects.all()
    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': "🧑‍🎤 Artistes"
    })

def show(request, artist_id):
    artist = get_object_or_404(Artist.objects.select_related('troupe'), pk=artist_id)

    is_admin = request.user.is_authenticated and request.user.is_admin
    form_troupe = None

    if is_admin:
        if request.method == "POST":
            form_troupe = ArtistTroupeForm(request.POST, instance=artist)
            if form_troupe.is_valid():
                form_troupe.save()
                messages.success(request, "✅ Troupe modifiée avec succès.")
                return redirect('catalogue:artist-show', artist.id)
            else:
                messages.error(request, "❌ Erreur lors de la modification de la troupe.")
        else:
            form_troupe = ArtistTroupeForm(instance=artist)

    # récupère les autres infos habituelles
    types = artist.artiste_type.select_related("type")
    participations = ArtistTypeShow.objects.filter(artist_type__artist=artist).select_related(
        "artist_type__type", "show"
    )

    return render(request, "artist/show.html", {
        "artist": artist,
        "types": types,
        "participations": participations,
        "form_troupe": form_troupe,
        "is_admin": is_admin,
        "title": f"🎭 {artist}"
    })


@login_required
def create(request):
    is_admin = request.user.is_authenticated and request.user.is_admin

    if request.method == "POST":
        form = ArtistForm(request.POST)
        if not is_admin:
            form.fields.pop('troupe')  # Retirer le champ troupe pour non-admin

        if form.is_valid():
            form.save()
            messages.success(request, "✅ Artiste ajouté avec succès.")
            return redirect('catalogue:artist-index')
        else:
            messages.error(request, "❌ Une erreur est survenue. Veuillez vérifier le formulaire.")
    else:
        form = ArtistForm()
        if not is_admin:
            form.fields.pop('troupe')

    return render(request, 'artist/form.html', {
        'form': form,
        'title': "➕ Ajouter un artiste",
        'is_admin': is_admin,
    })

@login_required
def edit(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    is_admin = request.user.is_authenticated and request.user.is_admin

    if request.method == "POST":
        # Si admin, formulaire complet avec troupe, sinon formulaire sans troupe
        if is_admin:
            form = ArtistForm(request.POST, instance=artist)
        else:
            # Formulaire sans troupe pour non-admin
            data = request.POST.copy()
            data.pop('troupe', None)  # retirer le champ troupe si présent pour éviter erreur
            form = ArtistForm(data, instance=artist)
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

@login_required
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
