from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalogue.forms import ArtistTypeShowForm
from catalogue.models import ArtistTypeShow

@login_required
def create(request):
    form = ArtistTypeShowForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Participation artistique crée.")
        return redirect('catalogue:artist-type-show-index')
    return render(request, "artist_type_show/form.html", {
        "form": form,
        "title": "🎭 Lier une participation à un spectacle"
    })

@login_required
def index(request):
    links = ArtistTypeShow.objects.select_related("artist_type__artist", "artist_type__type", "show")
    return render(request, "artist_type_show/index.html", {
        "links": links,
        "title": "🎬 Participations artistiques par spectacle"
    })

@login_required
def edit(request, id):
    link = get_object_or_404(ArtistTypeShow, pk=id)
    form = ArtistTypeShowForm(request.POST or None, instance=link)
    if form.is_valid():
        form.save()
        messages.success(request, "✅ Participation artistique modifiée.")
        return redirect('catalogue:artist-type-show-index')
    return render(request, "artist_type_show/form.html", {
        "form": form,
        "title": "✏️ Modifier une participation artistique"
    })

def delete(request, id):
    link = get_object_or_404(ArtistTypeShow, pk=id)

    if request.method == "POST":
        link.delete()
        messages.success(request, "🗑 Participation artistique supprimée.")
        return redirect('catalogue:artist-type-show-index')

    return render(request, "artist_type_show/delete.html", {
        "link": link,
        "title": f"🗑 Supprimer la participation de {link.artist_type} dans « {link.show.title} »"
    })
