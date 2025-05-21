from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalogue.models import Show, ArtistTypeShow
from catalogue.forms import ShowForm

def index(request):
    shows = Show.objects.select_related("location").all()
    return render(request, "show/index.html", {
        "title": "🎬 Films",
        "shows": shows,
    })

def show(request, slug):
    show = get_object_or_404(Show, slug=slug)
    representations = show.representations.all()
    reviews = show.reviews.select_related("user").all()

    participations = ArtistTypeShow.objects.filter(show=show).select_related(
        "artist_type__artist", "artist_type__type"
    )

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    return render(request, "show/show.html", {
        "title": f"🎭 {show.title}",
        "show": show,
        "representations": representations,
        "reviews": reviews,
        "user_review": user_review,
        "participations": participations
    })

def create(request):
    if request.method == "POST":
        form = ShowForm(request.POST)
        if form.is_valid():
            show = form.save()
            messages.success(request, "✅ Spectacle ajouté.")
            return redirect("catalogue:show-show", show.slug)
        messages.error(request, "❌ Erreur lors de la création.")
    else:
        form = ShowForm()

    return render(request, "show/form.html", {
        "form": form,
        "title": "➕ Ajouter un spectacle",
    })

def edit(request, slug):
    show = get_object_or_404(Show, slug=slug)

    if request.method == "POST":
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Spectacle modifié avec succès.")
            return redirect("catalogue:show-show", form.instance.slug)
        messages.error(request, "❌ Erreur lors de la modification.")
    else:
        form = ShowForm(instance=show)

    return render(request, "show/form.html", {
        "form": form,
        "title": f"✏️ Modifier : {show.title}",
    })

def delete(request, slug):
    show = get_object_or_404(Show, slug=slug)

    if request.method == "POST":
        show.delete()
        messages.success(request, "🗑 Spectacle supprimé avec succès.")
        return redirect("catalogue:show-index")

    return render(request, "show/delete.html", {
        "show": show,
        "title": f"🗑 Supprimer : {show.title}",
    })
